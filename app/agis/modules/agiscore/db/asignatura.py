#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.asignatura.id.readable=False
    return tools.manejo_simple( db.asignatura )


def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr( db,'asignatura' ):
        db.define_table( 'asignatura',
            Field( 'abreviatura','string',length=4 ),
            Field( 'nombre','string',length=20 ),
            format="%(abreviatura)s - %(nombre)s"
            )
        db.asignatura.abreviatura.label=T( 'Abreviatura' )
        db.asignatura.abreviatura.required=True
        db.asignatura.abreviatura.requires=[IS_NOT_EMPTY(error_message=T('Información requerida')),IS_UPPER()]
        db.asignatura.abreviatura.requires.append(
            IS_NOT_IN_DB( db,'asignatura.abreviatura',error_message=T( '' ) )
            )
        db.asignatura.nombre.label=T('Nombre')
        db.asignatura.nombre.requires=[IS_NOT_EMPTY(error_message=T('Información requerida')),IS_UPPER()]
        db.commit()
