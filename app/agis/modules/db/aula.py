#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import edificio
from applications.agis.modules import tools

def sumar_capacidades(a1, a2):
    """Toma 2 aulas y retorna la suma de sus capacidades"""
    v1 = 0
    try:
        v1 = a1.capacidad
    except:
        v1 = a1
    v2 = 0
    try:
        v2 = a2.capacidad
    except:
        v2 = a2
    return v1 + v2

def capacidad_total(lista_aulas):
    """Dada una lista de aulas, retorna la capacidad total de estas"""
    definir_tabla()
    if not lista_aulas:
        # si no hay aulas
        return 0
    return reduce(sumar_capacidades, lista_aulas)

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
            format="%(nombre)s",
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
