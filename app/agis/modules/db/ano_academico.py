#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from gluon import *
from applications.agis.modules import tools
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import escuela

def obtener_manejo():
    db = current.db
    db.ano_academico.id.readable = False
    return tools.manejo_simple(db.ano_academico, [db.ano_academico.nombre])

def ano_actual():
    ahora = datetime.now()
    return str(ahora.year)

def buscar_actual(unidad_organica_id = None):
    db = current.db
    if not hasattr( db,'ano_academico' ): definir_tabla() # para evitar la recursividad con definir_tabla
    if not unidad_organica_id:
        unidad_organica_id = (escuela.obtener_sede_central()).id
    actual_nombre = ano_actual()
    query = ((db.ano_academico.nombre == actual_nombre) &
             (db.ano_academico.unidad_organica_id == unidad_organica_id))
    return db(query).select().first()

def definir_tabla():
    db = current.db
    T = current.T
    unidad_organica.definir_tabla()
    if not hasattr( db,'ano_academico' ):
        db.define_table( 'ano_academico',
            Field( 'nombre','string',length=4,required=True ),
            Field( 'descripcion','text',length=200,required=False ),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format="%(nombre)s",
            )
        db.ano_academico.nombre.requires = [ IS_INT_IN_RANGE(1900, 2300,
            error_message=T( 'Año incorrecto, debe estar entre 1900 y 2300' )
            )]
        db.ano_academico.nombre.requires.extend( tools.requerido )
        db.ano_academico.nombre.comment = T( 'En el formato AAAA' )
        db.ano_academico.nombre.label = T( 'Año Académico' )
        db.ano_academico.descripcion.label = T( 'Descripción' )
        db.ano_academico.unidad_organica_id.label = T('Unidad Orgánica')
        db.commit()
#     actual = buscar_actual()
#     if not actual:
#         # crear un año academico
#         unidad_organica_id = (escuela.obtener_sede_central()).id
#         nombre = ano_actual()
#         db.ano_academico.insert(nombre=nombre,unidad_organica_id=unidad_organica_id)
#         db.commit()
