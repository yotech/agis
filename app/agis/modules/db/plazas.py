#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import regimen_uo
from applications.agis.modules import tools

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
            Field( 'cantidad','integer' ),
            )
        db.plazas.ano_academico_id.label=T( 'Año académico' )
        db.plazas.carrera_id.label=T( 'Carrera' )
        db.plazas.regimen_id.label=T( 'Regimén' )
        db.plazas.cantidad.label=T( 'Cantidad de plazas' )
        db.plazas.cantidad.default=20
        db.plazas.cantidad.required=True
        db.plazas.cantidad.reqires=IS_INT_IN_RANGE( 1,100,error_message='Debe estar entre 1 y 100' )
        db.commit()
