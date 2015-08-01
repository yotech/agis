#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import evento
from applications.agis.modules.db import aula
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import candidatura_carrera
from applications.agis.modules.db import plan_curricular
from applications.agis.modules.db import asignatura_plan

EXAMEN_TIPO_VALUES = [
    ('1', 'Acceso'),
]
def examen_tipo_represent(valor, fila):
    for i in EXAMEN_TIPO_VALUES:
        if i[0] == valor:
            return current.T(i[1])
    return current.T('N/D')

EXAMEN_PERIODO_VALUES = [
    ('1', 'Mañana'),
    ('2', 'Tarde'),
    ('3', 'Noche'),
]
def examen_periodo_represent(valor, fila):
    for i in EXAMEN_PERIODO_VALUES:
        if i[0] == valor:
            return current.T(i[1])
    return current.T('N/D')

def examen_format(fila):
    db = current.db
    asig = db.asignatura[fila.asignatura_id].nombre
    return '{0} - {1}'.format(asig, fila.fecha if fila.fecha else 'N/D')
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
        print request.vars
        if not 'e_id' in request.vars:
            return False
        asignatura_id = int(value)
        evento_id = int(request.vars.e_id)
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

def generar_examenes_acceso(cand):
    """Dada una candidatura (cand) crea - si no existen - los examenes que tiene que realizar
    el candidato.
    """
    db = current.db
    definir_tabla()
    candidatura.definir_tabla()
    candidatura_carrera.definir_tabla()
    plan_curricular.definir_tabla()
    asignatura_plan.definir_tabla()
    assert hasattr(cand, 'id')
    # ID's de todas las carreras seleccionadas en la candidatura
    carreras_ids = candidatura_carrera.obtener_carreras([cand])
    planes = plan_curricular.obtener_para_carreras( carreras_ids )
    # Asignaturas que cand debe examinar para las carreras que selecciona
    asig = asignatura_plan.asignaturas_por_planes( planes )
    # buscar el evento inscripción para la candidatura.
    ev = candidatura.obtener_evento(cand)
    assert hasattr(ev, 'id')
    for a in asig:
        # Para cada asignatura se debe crear un examen si este no existe ya.
        ex = db((db.examen.asignatura_id == a.id) &
                (db.examen.evento_id == ev.id ) &
                (db.examen.tipo == '1') # examen de tipo acceso
               ).select().first()
        if not ex:
            # crear el examen.
            db.examen.insert(asignatura_id=a.id, tipo='1',evento_id=ev.id)
            db.commit()

def obtener_aulas(examen_id):
    """Retorna la lista de aulas definidas para un examen"""
    db = current.db
    definir_tabla()
    ex = db.examen(examen_id)
    assert ex != None
    return db((db.aula.id == db.examen_aula.aula_id) &
              (db.examen_aula.examen_id == ex.id)
             ).select(db.aula.ALL)

def obtener_candidaturas(examen_id):
    """Retorna el listado de candidatos que deben realizar el examen con examen_id

    la lista retornada son los ID's de las candidaturas.
    """
    db = current.db
    definir_tabla()
    ex = db.examen(examen_id)
    assert ex != None
    evento = db.evento(ex.evento_id)
    asig = db.asignatura(ex.asignatura_id)
    # buscar los planes academicos que incluyan la asignatura en nivel académico de acceso.
    planes = db((db.plan_curricular.id == db.asignatura_plan.plan_curricular_id) &
                (db.plan_curricular.estado == True) &
                (db.asignatura_plan.asignatura_id == asig.id) &
                ((db.asignatura_plan.nivel_academico_id == db.nivel_academico.id) &
                 (db.nivel_academico.nivel=='0'))
               ).select(db.plan_curricular.id,distinct=True)
    # carreras a las que pertenecen estos planes
    carreras = list(set([db.plan_curricular(plan.id).carrera_id for plan in planes]))
    candidaturas = db(((db.candidatura.id == db.candidatura_carrera.candidatura_id) &
                       (db.candidatura_carrera.carrera_id.belongs(carreras))) &
                      (db.candidatura.estado_candidatura == '2') &
                      (db.candidatura.ano_academico_id == evento.ano_academico_id)
                     ).select(db.candidatura.id,distinct=True)
    return candidaturas

def definir_tabla():
    db = current.db
    T = current.T
    asignatura.definir_tabla()
    evento.definir_tabla()
    aula.definir_tabla()
    if not hasattr(db, 'examen'):
        db.define_table('examen',
            Field('asignatura_id', 'reference asignatura', notnull=True, required=True),
            Field('evento_id', 'reference evento'),
            Field('tipo', 'string', length=1),
            Field('fecha', 'date', notnull=False,default=None, required=False),
            Field('periodo','string',length=1, default=None, notnull=False, required=False),
            format=examen_format,
        )
        db.commit()
    if not hasattr(db, 'examen_aula'):
        db.define_table('examen_aula',
            Field('examen_id','reference examen'),
            Field('aula_id','reference aula'),
            format=examen_aula_format,
        )
        db.commit()
    db.examen.asignatura_id.label = T('Asignatura')
    db.examen.evento_id.label = T('Evento')
    db.examen.tipo.label = T('Tipo de examen')
    db.examen.tipo.represent = examen_tipo_represent
    db.examen.tipo.requires = IS_IN_SET(EXAMEN_TIPO_VALUES, zero=None)
    db.examen.fecha.label = T('Fecha')
    db.examen.fecha.represent = lambda v,r: 'N/D' if not v else v
    db.examen.periodo.label = T('Periodo')
    db.examen.periodo.represent = examen_periodo_represent
    db.examen.periodo.requires = IS_IN_SET(EXAMEN_PERIODO_VALUES, zero=None)
    db.examen_aula.examen_id.label = T('Examen')
    db.examen_aula.aula_id.label = T('Sala de aula')
