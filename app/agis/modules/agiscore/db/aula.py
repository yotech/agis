#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import edificio
from agiscore import tools

def capacidad_total(lista_aulas):
    """Dada una lista de aulas, retorna la capacidad total de estas"""
    definir_tabla()
    capacidad = 0
    for a in lista_aulas:
        capacidad += a.capacidad
    return capacidad

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.aula.id.readable = False
    return tools.manejo_simple(db.aula)

def aula_format(row):
#     db = current.db
#     ed = db.edificio(row.edificio_id)
    return row.nombre

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
            format=aula_format,
            )
        db.aula.nombre.label = T( 'Nombre' )
        db.aula.nombre.required = True
        db.aula.nombre.requires = [IS_NOT_EMPTY(error_message=current.T('Información requerida')),
                                   IS_UPPER()]
        db.aula.nombre.requires.append(
            IS_NOT_IN_DB( db,'aula.nombre',error_message=T( 'Ya existe' ) )
            )
        db.aula.capacidad.label = T( 'Capacidad' )
        db.aula.edificio_id.label = T( 'Edificio' )
        db.aula.edificio_id.requires = IS_IN_DB( db,'edificio.id','%(abreviatura)s-%(nombre)s',zero=None )
        db.aula.disponible.label = T( '¿Disponible?' )
        db.commit()
