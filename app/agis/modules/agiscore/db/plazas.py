#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import ano_academico
from agiscore.db import carrera_uo
from agiscore.db import regimen_uo
from agiscore import tools

def buscar_plazas(ano_academico_id, regimen_id, carrera_id):
    # busca la plaza correspondiente a Año, Carrera y Regimen y si no
    # existe se crea la misma.
    db = current.db
    p = db((db.plazas.id > 0) & 
              (db.plazas.ano_academico_id == ano_academico_id) & 
              (db.plazas.carrera_id == carrera_id) & 
              (db.plazas.regimen_id == regimen_id)).select().first()
    if not p:
        id = db.plazas.insert(ano_academico_id=ano_academico_id,
                              carrera_id=carrera_id,
                              regimen_id=regimen_id)
        db.commit()
        p = db.plazas(id)
    return p

def obtener_manejo():
    db = current.db
    db.plazas.id.readable = False
    return tools.manejo_simple(db.plazas)

def _before_update(s, f):
    if f['necesarias'] > f['maximas']:
        f['maximas'] = f['necesarias']

def definir_tabla():
    db = current.db
    T = current.T
    ano_academico.definir_tabla()
    carrera_uo.definir_tabla()
    regimen_uo.definir_tabla()
    if not hasattr(db, 'plazas'):
        db.define_table('plazas',
            Field('ano_academico_id', 'reference ano_academico'),
            Field('carrera_id', 'reference carrera_uo'),
            Field('regimen_id', 'reference regimen_unidad_organica'),
            Field('necesarias', 'integer'),
            Field('maximas', 'integer'),
            Field('media', 'double'),
            )
        db.plazas._before_update.append(_before_update)
        db.plazas.ano_academico_id.label = T('Año académico')
        db.plazas.carrera_id.label = T('Carrera')
        db.plazas.regimen_id.label = T('Regimén')
        db.plazas.necesarias.label = T('Plazas necesarias')
        db.plazas.necesarias.default = 0
        db.plazas.necesarias.required = True
        db.plazas.maximas.label = T('Plazas máximas')
        db.plazas.maximas.default = 0
        db.plazas.media.label = T('Media mínima')
        db.plazas.media.requires = IS_FLOAT_IN_RANGE(0, 20,
            error_message=T('Debe ser un valor entre 0 y 20'))
        db.plazas.media.default = 0.0
        db.commit()
