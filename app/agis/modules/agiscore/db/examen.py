#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import asignatura
from agiscore.db import evento
from agiscore.db import aula
from agiscore.db import candidatura
from agiscore.db import candidatura_carrera
from agiscore.db import plan_curricular
from agiscore.db import asignatura_plan

EXAMEN_TIPO_VALUES = [
    ('1', 'ACCESO'),
]
def examen_tipo_represent(valor, fila):
    for i in EXAMEN_TIPO_VALUES:
        if i[0] == valor:
            return current.T(i[1])
    return current.T('N/D')

# ~ EXAMEN_PERIODO_VALUES = [
    # ~ ('1', 'MANHÃ'),
    # ~ ('2', 'TARDE'),
    # ~ ('3', 'NOITE'),
# ~ ]
# ~ def examen_periodo_represent(valor, fila):
    # ~ for i in EXAMEN_PERIODO_VALUES:
        # ~ if i[0] == valor:
            # ~ return current.T(i[1])
    # ~ return current.T('N/D')

def examen_format(fila):
    db = current.db
#     ev = db.evento(fila.evento_id)
    asig = db.asignatura(fila.asignatura_id).nombre
    return asig
#     return '{0} - {1}'.format(asig, ev.nombre)
def examen_aula_format(fila):
    db = current.db
    ex = examen_format(db.examen[fila.examen_id])
    a = db.aula[fila.aula_id].nombre
    return '{0} - {1}'.format(ex, a)

class ExamenAsignaturaIdValidator(object):

    def __init__(self, error_message="Ya existe un examen para la asignatura"):
        T = current.T
        self.e = T(error_message)

    def validate(self, value):
        db = current.db
        request = current.request
        # print request.vars
        if not 'evento_id' in request.vars:
            return False
        asignatura_id = int(value)
        evento_id = int(request.vars.evento_id)
        query = (db.examen.asignatura_id == asignatura_id) & (db.examen.evento_id == evento_id)
        if 'id' in request.vars:
            # es una edición
            query &= (db.examen.id != int(request.vars.id))
        hay = db(query).select()
        if hay:
            return False

        return True

    def parsed(self, value):
        return value

    def __call__(self, value):
        if self.validate(value):
            return (self.parsed(value), None)
        else:
            return (value, self.e)

def examenesAccesoPorCarrera(carrera_id, evento_id):
    """
    Retorna listado de examenes que se deben realizar
    en el nivel acceso para la carrera.
    """
    db = current.db
    asig_set = plan_curricular.obtenerAsignaturasAcceso(carrera_id)
    exs = []
    for a in asig_set:
        q = (db.examen.asignatura_id == a)
        q &= (db.examen.evento_id == evento_id)
        e = db(q).select(cache=(current.cache.ram, 300), cacheable=True).first()
        exs.append(e)
    return exs

def generar_examenes_acceso_ex(ev, db=None):
    if db is None:
        db = current.db
    assert ev is not None
    # todo cambiar '1' por una constante
    assert ev.tipo == '1'
    ano = db.ano_academico(ev.ano_academico_id)
    query =  (db.candidatura.ano_academico_id == ano.id)
    query &= (db.candidatura_carrera.candidatura_id == db.candidatura.id)
    c_list = db(query).select(db.candidatura_carrera.carrera_id,
                              distinct=True,
                              cache=(current.cache.ram,300),
                              cacheable=True)
    carreras_ids = [r.carrera_id for r in c_list]
    
    # planes para esas carreras
    query = (db.plan_curricular.estado == True)
    query &= (db.plan_curricular.carrera_id.belongs(carreras_ids))
    p_res = db(query).select(db.plan_curricular.id,
                             distinct=True,
                             cache=(current.cache.ram,300),
                             cacheable=True)
    planes = [r.id for r in p_res]
    # Asignaturas que cand debe examinar para las carreras que selecciona
    from agiscore.db.nivel_academico import ACCESO
    query = db.asignatura_plan.plan_curricular_id.belongs(planes)
    query &= (db.asignatura_plan.nivel_academico_id == db.nivel_academico.id)
    query &= (db.nivel_academico.nivel == ACCESO)
    # asig = asignatura_plan.asignaturas_por_planes(planes, nivel=ACCESO)
    a_res = db(query).select(db.asignatura_plan.asignatura_id,
                             distinct=True,
                             cache=(current.cache.ram,300),
                             cacheable=True)
    asig = [r.asignatura_id for r in a_res]

    lista_examenes = list()
    for a in asig:
        # Para cada asignatura se debe crear un examen si este no existe ya.
        ex = db.examen(asignatura_id=a.id, evento_id=ev.id, tipo='1')
        if ex is None:
            # crear el examen.
            e_id = db.examen.insert(asignatura_id=a.id, tipo='1', evento_id=ev.id)
            lista_examenes.append(e_id)
        else:
            lista_examenes.append(ex.id)
    return lista_examenes

# def generar_examenes_acceso(cand, evento_id=None, db=None):
#     """Dada una candidatura (cand) crea - si no existen - los examenes que
#     tiene que realizar el candidato.
# 
#     retorna una lista con los ID's los examenes creados o encontrados
#     """
#     if db is None:
#         db = current.db
#     assert cand is not None
#     # carreras
#     # carreras_ids = candidatura_carrera.obtener_carreras([cand])
#     query = (db.candidatura_carrera.candidatura_id == cand.id)
#     c_list = db(query).select(db.candidatura_carrera.carrera_id,
#                               distinct=True,
#                               cache=(current.cache.ram,300),
#                               cacheable=True)
#     carreras_ids = [r.carrera_id for r in c_list]
#     
#     # planes para esas carreras
#     query = (db.plan_curricular.estado == True)
#     query &= (db.plan_curricular.carrera_id.belongs(carreras_ids))
#     p_res = db(query).select(db.plan_curricular.id,
#                              distinct=True,
#                              cache=(current.cache.ram,300),
#                              cacheable=True)
#     planes = [r.id for r in p_res]
#     # Asignaturas que cand debe examinar para las carreras que selecciona
#     from agiscore.db.nivel_academico import ACCESO
#     query = db.asignatura_plan.plan_curricular_id.belongs(planes)
#     query &= (db.asignatura_plan.nivel_academico_id == db.nivel_academico.id)
#     query &= (db.nivel_academico.nivel == ACCESO)
#     # asig = asignatura_plan.asignaturas_por_planes(planes, nivel=ACCESO)
#     a_res = db(query).select(db.asignatura_plan.asignatura_id,
#                              distinct=True,
#                              cache=(current.cache.ram,300),
#                              cacheable=True)
#     asig = [r.asignatura_id for r in a_res]
#     # buscar el evento inscripción para la candidatura.
#     if evento_id is None:
#         ev = candidatura.obtener_evento(cand)
#     else:
#         ev = db.evento(evento_id)
#     assert ev is not None
#     lista_examenes = list()
#     print asig
#     for a in asig:
#         # Para cada asignatura se debe crear un examen si este no existe ya.
#         ex = db.examen(asignatura_id=a.id, evento_id=ev.id, tipo='1')
#         if ex is None:
#             # crear el examen.
#             id = db.examen.insert(asignatura_id=a.id, tipo='1', evento_id=ev.id)
#             lista_examenes.append(id)
#         else:
#             lista_examenes.append(ex.id)
#     return lista_examenes

def obtener_aulas(examen_id):
    """Retorna la lista de aulas definidas para un examen"""
    db = current.db
    ex = db.examen(examen_id)
    return db((db.aula.id == db.examen_aula.aula_id) & 
              (db.examen_aula.examen_id == ex.id)
             ).select(db.aula.ALL)

def obtener_candidaturas(examen_id):
    """Retorna el listado de candidatos que deben realizar el examen con
       examen_id
    """
    db = current.db
    ex = db.examen(examen_id)
    assert ex != None
    evento = db.evento(ex.evento_id)
    asig = db.asignatura(ex.asignatura_id)
    # buscar los planes academicos que incluyan la asignatura en nivel académico de acceso.
    planes = db((db.plan_curricular.id == db.asignatura_plan.plan_curricular_id) & 
                (db.plan_curricular.estado == True) & 
                (db.asignatura_plan.asignatura_id == asig.id) & 
                ((db.asignatura_plan.nivel_academico_id == db.nivel_academico.id) & 
                 (db.nivel_academico.nivel == '0'))
               ).select(db.plan_curricular.id, distinct=True,
                        cache=(current.cache.ram, 300), cacheable=True)
    # carreras a las que pertenecen estos planes
    estados = [candidatura.ADMITIDO,
               candidatura.NO_ADMITIDO,
               candidatura.INSCRITO]
    carreras = list(set([db.plan_curricular(plan.id).carrera_id for plan in planes]))
    candidaturas = db(((db.candidatura.id == db.candidatura_carrera.candidatura_id) & 
                       (db.candidatura_carrera.carrera_id.belongs(carreras))) & 
                      (db.candidatura.estado_candidatura.belongs(estados)) & 
                      (db.candidatura.ano_academico_id == evento.ano_academico_id)
                     ).select(db.candidatura.id, distinct=True,
                              cache=(current.cache.ram, 300), cacheable=True)
    return candidaturas

def definir_tabla():
    db = current.db
    T = current.T
    asignatura.definir_tabla()
    evento.definir_tabla()
    aula.definir_tabla()
    if not hasattr(db, 'examen'):
        db.define_table('examen',
            Field('asignatura_id',
                  'reference asignatura',
                  notnull=True,
                  required=True),
            Field('evento_id', 'reference evento'),
            Field('tipo', 'string', length=1),
            Field('fecha', 'date', notnull=False, default=None, required=False),
            Field('inicio', 'time', label=T("Hora de incio")),
            Field('fin', 'time', label=T("Hora de finalización")),
            # ~ Field('periodo','string', length=17),
            format=examen_format,
        )
        db.commit()
    if not hasattr(db, 'examen_aula'):
        db.define_table('examen_aula',
            Field('examen_id', 'reference examen'),
            Field('aula_id', 'reference aula'),
            format=examen_aula_format,
        )
        db.commit()
    db.examen.asignatura_id.label = T('Asignatura')
    db.examen.evento_id.label = T('Evento')
    db.examen.tipo.label = T('Tipo de examen')
    db.examen.tipo.represent = examen_tipo_represent
    db.examen.tipo.requires = IS_IN_SET(EXAMEN_TIPO_VALUES, zero=None)
    db.examen.fecha.label = T('Fecha')
    db.examen.fecha.represent = lambda v, r: 'N/D' if v is None else v
    db.examen.inicio.represent = lambda v, r: 'N/D' if v is None else v
    db.examen.fin.represent = lambda v, r: 'N/D' if v is None else v
    # ~ db.examen.periodo.label = T('Periodo')
    # periodo = "HH:MM:SS-HH:MM:SS"
    # ~ db.examen.periodo.represent = examen_periodo_represent
    # ~ db.examen.periodo.requires = IS_IN_SET(EXAMEN_PERIODO_VALUES, zero=None)
    db.examen_aula.examen_id.label = T('Examen')
    db.examen_aula.aula_id.label = T('Sala de aula')
