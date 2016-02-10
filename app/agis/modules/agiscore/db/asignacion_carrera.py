# -*- coding: utf-8 -*-
from gluon import *
from Queue import PriorityQueue
from agiscore.db import carrera_uo
from agiscore.db import candidatura
from agiscore.db import evento
from agiscore.db.nota import obtenerResultadosAcceso
from agiscore.db.candidatura_carrera import obtenerCandidaturasPorCarrera


class Carrera(object):

    def __init__(self, maximas, minimas, mediaMinima, cid):
        self.maximas = maximas
        self.minimas = minimas
        self.mediaMinima = mediaMinima
        self.cid = cid  # identificador de la carrera
        self.admitidos = PriorityQueue()

    def probarMinimas(self):
        return len(self.admitidos.queue) >= self.minimas

    def admitir(self, c, media_candidato):
        assert isinstance(c, Candidato)

        # si esta llena no se puede admitir a más nadie
        if self.estaLlena():
            # si esta llena hay que empujar el nuevo valor y sacar el primero 
            # de la cola, si es el mismo candidato no se admite, si es otro
            # retornarlo
            self.admitidos.put((media_candidato, c))
            # sacar el que tenga menor promedio
            (m_tmp, c_tmp) = self.admitidos.get()
            if c_tmp.cid != c.cid:
                return c_tmp
            
            # si es el mismo que acabo de empujar retornar False
            return False
        
        # si la carrera no fue configurada no admitir a nadie
        if self.maximas == 0:
            return False

        # si no se cumple con la media minima entonces no se admite
        if media_candidato < self.mediaMinima:
            return False

        self.admitidos.put((media_candidato, c))
        return c

    def estaLlena(self):
        return len(self.admitidos.queue) == self.maximas

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
        return "P:{2} C:{0} M:{1}".format(repr(self.carrera), self.media, self.prioridad)

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
        c = db(db.carrera_uo.id == carrera_id).select(cache=(current.cache.ram, 300),
                                                      cacheable=True).first()
        if c:
            q = (db.plazas.carrera_id == c.id)
            q &= (db.plazas.ano_academico_id == ano_academico_id)
            q &= (db.plazas.regimen_id == self.rid)
            plz = db(q).select(cache=(current.cache.ram, 300),
                               cacheable=True).first()
            if plz:
                r = Carrera(plz.maximas, plz.necesarias, plz.media, c.id)
                self.carreras.append(r)

        return r


class Factoria(object):
    """ una fabrica de objetos con cache """

    def __init__(self, evento_id, regimen_id, noIncluir):
        db = current.db
        self.evento = db.evento(evento_id)
        self.candidatos = list()
        self.regimen = Regimen(regimen_id)
        self.noIncluir = noIncluir  # lista de ID's de carreras a no tener en cuenta

    def obtenerCarrera(self, carrera_id):
        if self.regimen:
            return self.regimen.obtenerCarrera(carrera_id, self.evento.ano_academico_id)

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
        q = (db.candidatura_carrera.candidatura_id == cdata.id)
        q &= (~db.candidatura_carrera.carrera_id.belongs(self.noIncluir))
        ops = db(q).select(cache=(current.cache.ram, 300),
                           cacheable=True)
        opciones = list()
        for o in ops:
            c = self.obtenerCarrera(o.carrera_id)
            if c:
                m = obtenerResultadosAcceso(cdata.id, c.cid, self.evento.id)
                opciones.append(Opcion(c, o.prioridad, m))

        med = 0.0
        r = Candidato(cdata.id, med, opciones)
        self.candidatos.append(r)

        return r

    def obtenerRegimen(self):
        return self.regimen

def _asignarCarreras(evento_id, regimen_id, no_tener_en_cuenta=[]):
    """Intenta realizar la asignación de todas las carreras que participen en 
    el evento de inscripción evento_id
    """
    db = current.db
    e = db.evento(evento_id)
    assert ((e is not None) & (e.tipo == evento.INSCRIPCION))
    aa = db.ano_academico(e.ano_academico_id)
    uo = db.unidad_organica(aa.unidad_organica_id)
    carreras = db((db.carrera_uo.unidad_organica_id == uo.id) & 
                  (~db.carrera_uo.id.belongs(no_tener_en_cuenta))
                  ).select(cache=(current.cache.ram, 300), cacheable=True)
    factoria = Factoria(evento_id, regimen_id, no_tener_en_cuenta)

    # hacer una cola de prioridades que será el escalafon general
    escalafon = PriorityQueue()

    # buscar todas las candidaturas para el evento actual
    q = (db.candidatura.id > 0)
    q &= (db.candidatura.estado_candidatura != candidatura.INSCRITO_CON_DEUDAS)
#     q &= (db.candidatura.unidad_organica_id == uo.id)
    q &= (db.candidatura.ano_academico_id == aa.id)
    q &= (db.candidatura.regimen_id == regimen_id)
    candidaturas = db(q).select(db.candidatura.ALL,
                                orderby=db.candidatura.numero_inscripcion,
                                cache=(current.cache.ram, 300),
                                cacheable=True)
    # metemos en el escalafon cada uno de los candidatos
#     import cProfile
    for c in candidaturas:
#         profile = cProfile.Profile()
#         profile.enable()
        ca = factoria.obtenerCandidato(c.id)
        if not ca.opciones.empty():
            escalafon.put((-ca.opciones.queue[0].media, ca))
#         profile.disable()
#         profile.print_stats()

#     print "---"
#     print "ANTES DEL PROCESO:"
#     print factoria.candidatos


    # asignar carreras
    while not escalafon.empty():
        (m, c) = escalafon.get()  # candidato con la media más alta
        assert isinstance(c, Candidato)
#         print "ANALIZANDO CANDIDATO: ", c
        # para cada opcion tratar de admitirlo
        op = c.obtenerOpcion()
        if op:
            c2 = op.admitir(c)
            if c2 == c:
                # se le asigno la carrera.
                c.admitido = op
#                 print "ADMITIENDDO CANDIDATO: {0} EN {1}".format(c, op.carrera)
            else:
                # o no se admitio o desplazo a otro candidato en esa carrera
                if c2 is False:
                    # no admitio, devolver el candidato al escalfon con una opcion menos
    #                 print "NO ADMITIR {0} EN {1}".format(c, op.carrera)
                    if not c.opciones.empty():
                        escalafon.put((-c.opciones.queue[0].media, c))
                elif isinstance(c2, Candidato):
                    # si es un desplazado, ponerlo como no admitido y retornarlo
                    # a la cola
                    c2.admitido = False
                    if not c2.opciones.empty():
                        escalafon.put((-c2.opciones.queue[0].media, c2))
                    # pero c desplazo a c2, admitirlo
                    c.admitido = op
        else:
            # no lo quedan opciones al candidato
#             print "{0} NO ADMITIDO EN NINGUNA".format(c)
            pass

#     print "---"
#     print "DESPUES DEL PROCESO:"
#     print factoria.candidatos

    # probar que se cumplan las minismas para cada carrera.
    nocumplen = list()
    # print "PROBAR QUE SE CUMPLE LA MINIMA NECESARIA PARA CADA CARRERA"
    for c in carreras:
        car = factoria.obtenerCarrera(c.id)
        if car:
            if not car.probarMinimas():
#                 print "NO CUMPLE MINIMAS: {0}".format(car)
                nocumplen.append(car.cid)
    # intentarlo de nuevo sin tener en cuaenta las carreras que no cumplen las minimas necesarias
    if nocumplen:
#         print "REINICIANDO PROCESO SIN LAS CARRERAS:", nocumplen
        return _asignarCarreras(evento_id, regimen_id, no_tener_en_cuenta=nocumplen)
    else:
        # factoria.candidatos tiene los candidatos con su estado final, retornar eso
#         print "TERMINADO"
        return factoria.candidatos

def asignarCarreras(evento_id, regimen_id):
    db = current.db
    candidatos = _asignarCarreras(evento_id, regimen_id)
#     print "RESULTADO FINAL:"
#     print candidatos
#     actualizar la BD:
    for c in candidatos:
        assert isinstance(c, Candidato)
        # eliminar asignaciones previas
        db(db.asignacion_carrera.candidatura_id == c.cid).delete()
        if c.admitido:
            db(db.candidatura.id == c.cid).update(estado_candidatura=candidatura.ADMITIDO)
            # agregar asignacion
            db.asignacion_carrera.insert(candidatura_id=c.cid,
                                         carrera_id=c.admitido.carrera.cid,
                                         media=c.admitido.media)
        else:
            # cambiar a no admitido
            db(db.candidatura.id == c.cid).update(estado_candidatura=candidatura.NO_ADMITIDO)
    db.commit()


def definir_tabla():
    db = current.db
    T = current.T
    db.define_table('asignacion_carrera',
                    Field('carrera_id', 'reference carrera_uo'),
                    Field('candidatura_id', 'reference candidatura'),
                    Field('media', 'double', default=0.0),
                    )
    db.commit()
