# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore import tools
from agiscore.db import carrera_uo as model

def seleccionar_carrera(unidad_organica_id = None):
    """Genera un GRID para la selección de una carrera"""
    model.definir_tabla()
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    #context.asunto = T('Seleccione la carrera')
    query = (db.carrera_uo.id > 0)
    if unidad_organica_id:
        query &= (db.carrera_uo.unidad_organica_id == unidad_organica_id)
    query &= (db.carrera_uo.descripcion_id == db.descripcion_carrera.id)
    c = tools.selector(query,
        [db.carrera_uo.id, db.descripcion_carrera.nombre],
        'carrera_uo_id', tabla='carrera_uo')
    #response.title = context.unidad_organica.nombre + ' - ' + T('Carreras')
    #response.subtitle = T('Carreras')
    return c
