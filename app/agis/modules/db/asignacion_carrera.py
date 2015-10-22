# -*- coding: utf-8 -*-
from gluon import *
from Queue import PriorityQueue
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import evento
from applications.agis.modules.db.nota import obtenerResultadosAcceso, obtenerResultadosAccesoGenerales
from applications.agis.modules.db.candidatura_carrera import obtenerCandidaturasPorCarrera


class Carrera(object):

    def __init__(self, maximas, minimas, mediaMinima, cid):
        self.maximas = maximas
        self.minimas = minimas
        self.mediaMinima = mediaMinima
        self.cid = cid  # identificador de la carrera
        self.admitidos = list()

    def probarMinimas(self):
        return len(self.admitidos) >= self.minimas

    def admitir(self, c, media_candidato):
        assert isinstance(c, Candidato)

        # si esta llena no se puede admitir a más nadie
        if self.estaLlena():
            return False

        # si no se cumple con la media minima entonces no se admite
        if media_candidato < self.mediaMinima:
            return False

        self.admitidos.append(c)
        return True

    def estaLlena(self):
        return len(self.admitidos) == self.maximas

    def __str__(self):
        return "(C:{0} [MA:{1}, MI:{2}, M:{3}])".format(self.cid, self.maximas, self.minimas, self.mediaMinima)

    def __repr__(self):
        return self.__str__()


class Opcion(object):

    def __init__(self, carrera, prioridad, media=0.0):
        assert isinstance(carrera, Carrera)
        self.prioridad = prioridad
        self.carrera = carrera
        self.media = media

    def __cmp__(self, other):
        assert isinstance(other, Opcion)
        return cmp(self.prioridad, other.prioridad)

    def __repr__(self):
        return "C:{0} M:{1}".format(repr(self.carrera), self.media)

    def admitir(self, c):
        return self.carrera.admitir(c, self.media)


class Candidato(object):

    def __init__(self, cid, media, opciones=[]):
        super(Candidato, self).__init__()
        self.opciones = PriorityQueue()
        for p in opciones:
            assert isinstance(p, Opcion)
            self.opciones.put(p)
        self.media = media
        self.cid = cid
        self.admitido = False

    def ponerAdmitido(self):
        self.admitido = True

    def obtenerOpcion(self):
        if not self.opciones.empty():
            return self.opciones.get()

        return None

    # def obtenerMedia(self, carrera):
    #     for o in self.opciones.queue:
    #         if o.carrera == carrera:
    #             return o.media
    #
    #     return -1000.0

    def __cmp__(self, other):
        assert isinstance(other, Candidato)
        # solo comparar dos candidatos con la misma carrera
        if self.opciones.queue and other.opciones.queue:
            opmia = self.opciones.queue[0]
            opotro = other.opciones.queue[0]
            assert isinstance(opmia, Opcion)
            assert isinstance(opotro, Opcion)
            if opmia.carrera == opotro.carrera:
                return cmp(opotro.media, opmia.media)

        # return cmp(other.media, self.media)
        return 0

    def __str__(self):
        return "(CA ID:{0}, OP:{1}, S:{2})".format(str(self.cid), self.opciones.queue, self.admitido)

    def __repr__(self):
        return self.__str__()


class Regimen(object):

    def __init__(self, rid):
        self.rid = rid
        self.carreras = list()

    def obtenerCarrera(self, carrera_id, ano_academico_id):
        """
        Factoria para carreras

        :return: Carrera
        """
        r = None

        for c in self.carreras:
            if c.cid == carrera_id:
                return c

        db = current.db
        c = db.carrera_uo(carrera_id)
        if c:
            plz = db.plazas(carrera_id=c.id, ano_academico_id=ano_academico_id, regimen_id=self.rid)
            if plz:
                r = Carrera(plz.maximas, plz.necesarias, plz.media, c.id)
                self.carreras.append(r)

        return r


class Factoria(object):
    """ una fabrica de objetos con cache """

    def __init__(self, evento_id, noIncluir):
        db = current.db
        self.evento = db.evento(evento_id)
        self.candidatos = list()
        self.regimenes = list()
        self.noIncluir = noIncluir # lista de ID's de carreras a no tener en cuenta

    def obtenerCarrera(self, carrera_id, regimen_id):
        regimen = self.obtenerRegimen(regimen_id)

        if regimen:
            return regimen.obtenerCarrera(carrera_id, self.evento.ano_academico_id)

        return None

    def obtenerCandidato(self, candidatura_id):
        """
        Factoria para Candidato

        :param candidatura_id: int
        :param regimen_id: int
        :return: Candidato
        """

        db = current.db
        r = None
        for c in self.candidatos:
            if c.cid == candidatura_id:
                return c

        cdata = db.candidatura(candidatura_id)
        ops = db((db.candidatura_carrera.candidatura_id==cdata.id) &
                 (~db.candidatura_carrera.carrera_id.belongs(self.noIncluir))).select()
        opciones = list()
        for o in ops:
            c = self.obtenerCarrera(o.carrera_id, cdata.regimen_unidad_organica_id)
            m = obtenerResultadosAcceso(cdata.id, c.cid, self.evento.id)
            opciones.append(Opcion(c, o.prioridad, m))
        # med = obtenerResultadosAccesoGenerales(cdata.id, self.evento.id)
        med = 0.0
        r = Candidato(cdata.id, med, opciones)
        self.candidatos.append(r)

        return r

    def obtenerRegimen(self, regimen_id):
        r = None

        for v in self.regimenes:
            if v.rid == regimen_id:
                return v
        db = current.db
        rdata = db.regimen_unidad_organica(regimen_id)
        r = Regimen(rdata.id)
        self.regimenes.append(r)

        return r

def asignarCarreras(evento_id):
    db = current.db
    candidatos = _asignarCarreras(evento_id)
    print "RESULTADO FINAL:"
    print candidatos
    # actualizar la BD:
    for c in candidatos:
        assert isinstance(c, Candidato)
        # eliminar asignaciones previas
        db(db.asignacion_carrera.candidatura_id == c.cid).delete()
        if c.admitido:
            db(db.candidatura.id == c.cid).update(estado_candidatura=candidatura.ADMITIDO)
            # agregar asignacion
            db.asignacion_carrera.insert(candidatura_id=c.cid, carrera_id=c.admitido.cid)
        else:
            # cambiar a no admitido
            db(db.candidatura.id == c.cid).update(estado_candidatura=candidatura.NO_ADMITIDO)
    db.commit()

def _asignarCarreras(evento_id, no_tener_en_cuenta=[]):
    """Intenta realizar la asignación de todas las carreras que participen en el evento de inscripción evento_id"""
    db = current.db
    e = db.evento(evento_id)
    assert ((e is not None) & (e.tipo == evento.INSCRIPCION))
    aa = db.ano_academico(e.ano_academico_id)
    uo = db.unidad_organica(aa.unidad_organica_id)
    carreras = db((db.carrera_uo.unidad_organica_id == uo.id) &
                  (~db.carrera_uo.id.belongs(no_tener_en_cuenta))).select()
    regimenes = db(db.regimen_unidad_organica.unidad_organica_id == uo.id).select()
    factoria = Factoria(evento_id, no_tener_en_cuenta)

    # hacer una cola de prioridades que será el escalafon general
    escalafon = PriorityQueue()

    # buscar todas las candidaturas para el evento actual
    q = (db.candidatura.id > 0)
    q &= (db.candidatura.estado_candidatura != candidatura.INSCRITO_CON_DEUDAS)
    q &= (db.candidatura.unidad_organica_id == uo.id)
    q &= (db.candidatura.ano_academico_id == aa.id)
    candidaturas = db(q).select(db.candidatura.ALL)
    # metemos en el escalafon cada uno de los candidatos
    for c in candidaturas:
        escalafon.put(factoria.obtenerCandidato(c.id))

    print "---"
    print "ANTES DEL PROCESO:"
    print factoria.candidatos


    # asignar carreras
    while not escalafon.empty():
        c = escalafon.get() # candidato con la media más alta
        assert isinstance(c, Candidato)
        print "ANALIZANDO CANDIDATO: ", c
        # para cada opcion tratar de admitirlo
        op = c.obtenerOpcion()
        if op:
            if op.admitir(c):
                # se le asigno la carrera.
                c.admitido = op.carrera
                print "ADMITIENDDO CANDIDATO: {0} EN {1}".format(c, op.carrera)
            else:
                # no admitio, devolver el candidato al escalfon con una opcion menos
                print "NO ADMITIR {0} EN {1}".format(c, op.carrera)
                escalafon.put(c)
        else:
            # no lo quedan opciones al candidato
            print "{0} NO ADMITIDO EN NINGUNA".format(c)

    print "---"
    print "DESPUES DEL PROCESO:"
    print factoria.candidatos

    # probar que se cumplan las minismas para cada carrera.
    nocumplen = list()
    print "PROBAR QUE SE CUMPLE LA MINIMA NECESARIA PARA CADA CARRERA"
    for r in regimenes:
        for c in carreras:
            car = factoria.obtenerCarrera(c.id, r.id)
            if car:
                if not car.probarMinimas():
                    print "NO CUMPLE MINIMAS: {0}".format(car)
                    nocumplen.append(car.cid)
    # intentarlo de nuevo sin tener en cuaenta las carreras que no cumplen las minimas necesarias
    if nocumplen:
        print "REINICIANDO PROCESO SIN LAS CARRERAS:", nocumplen
        return _asignarCarreras(evento_id, no_tener_en_cuenta=nocumplen)
    else:
        # factoria.candidatos tiene los candidatos con su estado final, retornar eso
        print "TERMINADO"
        return factoria.candidatos


def definir_tabla():
    db = current.db
    T = current.T
    db.define_table('asignacion_carrera',
                    Field('carrera_id', 'reference carrera_uo'),
                    Field('candidatura_id', 'reference candidatura'),
                    )
    db.commit()
