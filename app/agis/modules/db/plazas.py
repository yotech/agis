#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import regimen_uo
from applications.agis.modules import tools

def buscar_plazas(ano_academico_id=None,regimen_id=None,carrera_id=None):
    definir_tabla()
    db = current.db
    return db((db.plazas.id > 0) &
              (db.plazas.ano_academico_id==ano_academico_id) &
              (db.plazas.carrera_id==carrera_id) &
              (db.plazas.regimen_id==regimen_id)).select().first()

def obtener_manejo():
    db=current.db
    definir_tabla()
    db.plazas.id.readable=False
    return tools.manejo_simple( db.plazas )

def definir_tabla():
    db=current.db
    T=current.T
    ano_academico.definir_tabla()
    carrera_uo.definir_tabla()
    regimen_uo.definir_tabla()
    if not hasattr( db,'plazas' ):
        db.define_table( 'plazas',
            Field( 'ano_academico_id','reference ano_academico' ),
            Field( 'carrera_id','reference carrera_uo' ),
            Field( 'regimen_id','reference regimen_unidad_organica' ),
            Field( 'necesarias','integer' ),
            Field('maximas', 'integer'),
            Field('media', 'double'),
            )
        db.plazas.ano_academico_id.label=T( 'Año académico' )
        db.plazas.carrera_id.label=T( 'Carrera' )
        db.plazas.regimen_id.label=T( 'Regimén' )
        db.plazas.necesarias.label=T( 'Plazas necesarias' )
        db.plazas.necesarias.default=0
        db.plazas.necesarias.required=True
        db.plazas.maximas.label=T( 'Plazas máximas' )
        db.plazas.maximas.default = 0
        db.plazas.media.label = T('Media mínima')
        db.plazas.media.default = 0.0
        db.commit()
