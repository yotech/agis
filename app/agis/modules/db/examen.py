#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import evento
from applications.agis.modules.db import aula

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
    return '{0} - {1}'.format(asig, fila.fecha)
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
        if not 'evento_id' in request.vars:
            return False
        asignatura_id = int(value)
        evento_id = int(request.vars.evento_id)
        hay = db((db.examen.asignatura_id == asignatura_id) &
                 (db.examen.evento_id == evento_id)).select()
        if hay:
            return False

        return True

def definir_tabla():
    db = current.db
    T = current.T
    asignatura.definir_tabla()
    evento.definir_tabla()
    aula.definir_tabla()
    db.define_table('examen',
        Field('asignatura_id', 'reference asignatura'),
        Field('evento_id', 'reference evento'),
        Field('tipo', 'string', length=1),
        Field('fecha', 'date'),
        Field('periodo','string',length=1),
        format=examen_format,
    )
    db.commit()
    db.define_table('examen_aula',
        Field('examen_id','reference examen'),
        Field('aula_id','reference aula'),
        format=examen_aula_format,
    )
    db.commit()
    db.examen.asignatura_id.label = T('Asignatura')
    #db.examen.asignatura_id.requires = [ExamenAsignaturaIdValidator()]
    db.examen.evento_id.label = T('Evento')
    db.examen.tipo.label = T('Tipo de examen')
    db.examen.tipo.represent = examen_tipo_represent
    db.examen.tipo.requires = IS_IN_SET(EXAMEN_TIPO_VALUES, zero=None)
    db.examen.fecha.label = T('Fecha')
    db.examen.periodo.label = T('Periodo')
    db.examen.periodo.represent = examen_periodo_represent
    db.examen.periodo.requires = IS_IN_SET(EXAMEN_PERIODO_VALUES, zero=None)
    db.examen_aula.examen_id.label = T('Examen')
    db.examen_aula.aula_id.label = T('Sala de aula')
