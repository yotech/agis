#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import campus
from agiscore import tools

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.edificio.id.readable = False
    return tools.manejo_simple(db.edificio)

def definir_tabla():
    db = current.db
    T = current.T
    campus.definir_tabla()
    if not hasattr( db,'edificio' ):
        db.define_table('edificio',
            Field( 'abreviatura','string',length=4 ),
            Field( 'nombre','string',length=30 ),
            Field( 'disponible','boolean',default=True ),
            Field( 'campus_id','reference campus' ),
            format="%(abreviatura)s",
            )
        db.edificio.abreviatura.label = T( 'Abreviatura' )
        db.edificio.abreviatura.required = True
        db.edificio.abreviatura.requires = [IS_NOT_EMPTY(error_message=current.T('Información requerida' ) ) ]
        db.edificio.abreviatura.requires.append(IS_UPPER())
        db.edificio.nombre.label = T('Nombre')
        db.edificio.nombre.required = True
        db.edificio.nombre.requires = [ IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) ]
        db.edificio.nombre.requires.append(IS_UPPER())
        db.edificio.disponible.label = T( '¿Disponible?' )
        db.edificio.campus_id.label = T( 'Campus' )
        db.edificio.campus_id.requires = IS_IN_DB( db,'campus.id','%(abreviatura)s',zero=None )
        db.commit()
