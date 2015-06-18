#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    db.ano_academico.id.readable = False
    return tools.manejo_simple(db.ano_academico, [db.ano_academico.nombre])

def ano_actual():
    ahora = datetime.now()
    return str(ahora.year)

def buscar_actual():
    db = current.db
    if not hasattr( db,'ano_academico' ): definir_tabla()
    actual_nombre = ano_actual()
    return db(db.ano_academico.nombre == actual_nombre).select().first()

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr( db,'ano_academico' ):
        db.define_table( 'ano_academico',
            Field( 'nombre','string',length=4,required=True ),
            Field( 'descripcion','string',length=200,required=False ),
            format="%(nombre)s",
            )
        db.ano_academico.nombre.requires = [ IS_INT_IN_RANGE(1900, 2300,
            error_message=T( 'Año incorrecto, debe estar entre 1900 y 2300' )
            )]
        db.ano_academico.nombre.requires.extend( tools.requerido )
        db.ano_academico.nombre.comment = T( 'En el formato AAAA' )
        db.ano_academico.nombre.label = T( 'Año Académico' )
        db.ano_academico.descripcion.label = T( 'Descripción' )
        db.commit()
    actual = buscar_actual()
    if not actual:
        # crear un año academico
        nombre = ano_actual()
        db.ano_academico.insert(nombre=nombre)
        db.commit()
