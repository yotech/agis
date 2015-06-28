#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db=current.db
    definir_tabla()
    db.nivel_academico.id.readable=False
    return tools.manejo_simple(db.nivel_academico)

def definir_tabla():
    db=current.db
    T=current.T

    if not hasattr( db,'nivel_academico' ):
        db.define_table( 'nivel_academico',
            Field( 'nombre','string',length=10 ),
        )
        db.nivel_academico.nombre.label=T( 'Nombre' )
        db.nivel_academico.nombre.unique=True
        db.nivel_academico.nombre.required=True
        db.nivel_academico.nombre.requires=[ IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ),
            IS_NOT_IN_DB( db,'nivel_academico.nombre',error_message=current.T( 'Ya existe' ) ),
        ]
        db.commit()
