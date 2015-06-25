#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import edificio
from applications.agis.modules import tools

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.aula.id.readable = False
    return tools.manejo_simple(db.aula)

def definir_tabla():
    db = current.db
    T = current.T
    edificio.definir_tabla()
    if not hasattr( db,'aula' ):
        db.define_table('aula',
            Field( 'nombre','string',length=15 ),
            Field( 'capacidad','integer',default=0 ),
            Field( 'edificio_id','reference edificio' ),
            Field( 'disponible','boolean',default=True ),
            )
        db.aula.nombre.label = T( 'Nombre' )
        db.aula.nombre.required = True
        db.aula.nombre.requires = [ IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) ]
        db.aula.capacidad.label = T( 'Capacidad' )
        db.aula.edificio_id.label = T( 'Edificio' )
        db.aula.edificio_id.requires = IS_IN_DB( db,'edificio.id','%(abreviatura)s-%(nombre)s',zero=None )
        db.aula.disponible.label = T( '¿Disponible?' )
        db.commit()
