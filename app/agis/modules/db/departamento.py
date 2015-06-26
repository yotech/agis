#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import unidad_organica
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.departamento.id.readable = False
    return tools.manejo_simple( db.departamento )

def definir_tabla():
    db = current.db
    T = current.T
    unidad_organica.definir_tabla()
    if not hasattr( db,'departamento' ):
        db.define_table( 'departamento',
            Field( 'nombre','string',length=20 ),
            Field( 'unidad_organica_id','reference unidad_organica' )
            )
        db.departamento.nombre.label=T( 'Nombre' )
        db.departamento.unidad_organica_id.label=T( 'Unidad organica' )
        db.departamento.unidad_organica_id.requires = IS_IN_DB( db,'unidad_organica.id',"%(nombre)s",zero=None )
        db.commit()
