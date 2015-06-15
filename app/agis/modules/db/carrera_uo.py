#!/usr/bin/env python
# -*- coding: utf-8 -*-
from applications.agis.modules.db import descripcion_carrera
from applications.agis.modules.db import unidad_organica
from gluon import *

def carrera_uo_format(fila):
    definir_tabla()
    db = current.db
    return db.descripcion_carrera[fila.descripcion_id].nombre

def obtener_posibles(unidad_organica_id):
    """
    Retorna una lista de las posibles carreras a agregar a la unidad organica
    """
    definir_tabla()
    db = current.db
    rows = db(db.carrera_uo.unidad_organica_id == None).select(
        db.descripcion_carrera.ALL, db.carrera_uo.ALL,
        orderby=db.descripcion_carrera.nombre,
        left=db.carrera_uo.on((db.descripcion_carrera.id == db.carrera_uo.descripcion_id)
                             &(db.carrera_uo.unidad_organica_id == unidad_organica_id)))
    pos = []
    for item in rows:
        pos.append( (item.descripcion_carrera.id, item.descripcion_carrera.nombre) )
    return pos

def definir_tabla():
    db = current.db
    T = current.T
    descripcion_carrera.definir_tabla()
    unidad_organica.definir_tabla()
    if not hasattr(db, 'carrera_uo'):
        db.define_table('carrera_uo',
            Field( 'descripcion_id','reference descripcion_carrera',required=True ),
            Field( 'unidad_organica_id','reference unidad_organica',required=True ),
            format=carrera_uo_format,
            plural=T( 'Carreras' ),
            singular=T( 'Carrera' ),
        )
        db.carrera_uo.descripcion_id.label=T( 'Descripción de la carrera' )
        db.carrera_uo.unidad_organica_id.label=T( 'Unidad organica' )
        db.commit()
