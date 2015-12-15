#!/usr/bin/env python
# -*- coding: utf-8 -*-
from agiscore.db import carrera_escuela
from agiscore.db import unidad_organica
from agiscore import tools
from gluon import *
from gluon.storage import Storage

def obtener_por_id(id):
    """ Retorna la carrera y su descripcion """
    db = current.db
    definir_tabla()
    db.carrera_uo.id.readable = False  # hide ID field
    return db((db.carrera_uo.id == id) & 
              (db.descripcion_carrera.id == db.carrera_uo.descripcion_id)
             ).select().first()

def seleccionar(context):
    """Genera un GRID para la selección de una carrera

    En context debe estar la unidad orgánica donde se selecciona
    la carrera.
    """
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    context.asunto = T('Seleccione la carrera')
    query = (db.carrera_uo.id > 0)
    query &= (db.carrera_uo.unidad_organica_id == context.unidad_organica.id)
    query &= (db.carrera_uo.descripcion_id == db.descripcion_carrera.id)
    context.manejo = tools.selector(query,
        [db.carrera_uo.id, db.descripcion_carrera.nombre],
        'carrera_uo_id', tabla='carrera_uo')
    response.title = context.unidad_organica.nombre + ' - ' + T('Carreras')
    response.subtitle = T('Carreras')
    return context

def obtener_selector(unidad_organica_id=None, enlaces_a=[]):
    # TODO: reimplementar esto usando tools.selector()
    db = current.db
    definir_tabla()
    if not unidad_organica_id:
        unidad_organica_id = (unidad_organica.obtener_por_escuela())[0].id
    query = ((db.carrera_uo.descripcion_id == db.descripcion_carrera.id) & 
            (db.carrera_uo.unidad_organica_id == unidad_organica_id))
    db.carrera_uo.id.readable = False
    return tools.manejo_simple(query, enlaces=enlaces_a, editable=False,
                               buscar=True, campos=[db.descripcion_carrera.nombre,
                                                   db.carrera_uo.id, ],
                               orden=[~db.descripcion_carrera.nombre],
                               crear=False, borrar=False)

def carrera_uo_format(fila):
    db = fila.update_record.db
    carr_esc = db.carrera_escuela(fila.carrera_escuela_id)
    return db.descripcion_carrera[carr_esc.descripcion_id].nombre

def obtener_carreras(unidad_organica_id):
    """da el conjunto de carreras de la unidad organica"""
    definir_tabla()
    db = current.db
    filas = db((db.carrera_uo.unidad_organica_id == unidad_organica_id) & 
        (db.carrera_uo.descripcion_id == db.descripcion_carrera.id)
    ).select()
    resultado = []
    for r in filas:
        resultado.append((r.carrera_uo.id, r.descripcion_carrera.nombre))
    return resultado

def obtener_posibles(db, unidad_organica_id):
    """
    Retorna una lista de las posibles carreras a agregar a la unidad organica
    """
    estan_query = (db.carrera_uo.id > 0)
    estan_query &= (db.carrera_uo.unidad_organica_id == unidad_organica_id)
    estan_rows = db(estan_query).select(db.carrera_uo.carrera_escuela_id)
    estan = [row.carrera_escuela_id for row in estan_rows]
    no_estan_query = (db.carrera_escuela.id > 0)
    no_estan_query &= (~(db.carrera_escuela.id.belongs(estan)))
    no_estan_query &= (db.carrera_escuela.descripcion_id == db.descripcion_carrera.id)
    no_estan_rows = db(no_estan_query).select(db.descripcion_carrera.nombre,
                                              db.carrera_escuela.id)
    posibles = [(i.carrera_escuela.id, i.descripcion_carrera.nombre) for i in no_estan_rows]
    return posibles

def definir_tabla():
    db = current.db
    T = current.T
    carrera_escuela.definir_tabla(db, T)
    # descripcion_carrera.definir_tabla()
    unidad_organica.definir_tabla()
    if not hasattr(db, 'carrera_uo'):
        tbl = db.define_table('carrera_uo',
            Field('carrera_escuela_id', 'reference carrera_escuela'),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format=carrera_uo_format,
            plural=T('Carreras'),
            singular=T('Carrera'),
        )
        tbl.id.readable = False
        tbl.carrera_escuela_id.label = T('Carrera IES')
        tbl.unidad_organica_id.label = T('Unidad organica')
