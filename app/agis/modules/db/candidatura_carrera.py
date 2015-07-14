#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import carrera_uo
from applications.agis.modules import tools

def obtener_manejo(candidatura_id):
    db = current.db
    definir_tabla()
    query = (db.candidatura_carrera.candidatura_id == candidatura_id)
    db.candidatura_carrera.id.readable = False
    db.candidatura_carrera.candidatura_id.readable = False
    db.candidatura_carrera.candidatura_id.writable = False
    crear = (db(query).count() <= 1)
    campos = [db.candidatura_carrera.carrera_id,
              db.candidatura_carrera.prioridad]
    orden = [db.candidatura_carrera.prioridad]
    return tools.manejo_simple(query,
                               campos=campos,
                               orden=orden,
                               crear=crear,
                               borrar=False)

def definir_tabla():
    db = current.db
    T = current.T
    candidatura.definir_tabla()
    carrera_uo.definir_tabla()
    if not hasattr( db, 'candidatura_carrera' ):
        db.define_table( 'candidatura_carrera',
            Field( 'candidatura_id','reference candidatura' ),
            Field( 'carrera_id','reference carrera_uo' ),
            Field( 'prioridad','integer',default=0 ),
            )
        db.candidatura_carrera.carrera_id.label = T('Carrera')
        db.candidatura_carrera.prioridad.label = T('Prioridad')
        db.commit()
