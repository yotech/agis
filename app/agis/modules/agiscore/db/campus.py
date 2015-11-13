#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools


def obtener_manejo():
    definir_tabla()
    db = current.db
    db.campus.id.readable = False
    return tools.manejo_simple(db.campus)


def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr( db,'campus' ):
        db.define_table( 'campus',
            Field( 'abreviatura','string',length=4 ),
            Field( 'nombre','string',length=30 ),
            Field( 'localizacion','text',length=200 ),
            Field( 'disponible','boolean',default=True ),
            format="%(abreviatura)s",
            )
        db.campus.abreviatura.label = T( 'Abreviatura' )
        db.campus.abreviatura.required = True
        db.campus.abreviatura.requires = [IS_NOT_EMPTY(error_message=current.T('Información requerida')),
                                          IS_UPPER()]
        db.campus.nombre.label = T( 'Nombre' )
        db.campus.nombre.required = True
        db.campus.nombre.requires = [IS_NOT_EMPTY(error_message=current.T('Información requerida')),
                                     IS_UPPER()]
        db.campus.localizacion.label = T('Localización')
        db.campus.localizacion.required = IS_UPPER()
        db.campus.disponible.label = T( '¿Disponible?' )
        db.commit()
