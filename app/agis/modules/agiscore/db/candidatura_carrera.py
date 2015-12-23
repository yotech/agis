#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import candidatura
from agiscore.db import carrera_uo
from agiscore import tools

def obtener_carreras(lita_candidaturas):
    """Retorna una lista con los ID's de todas las carreras presentes en la lista
       de candidaturas que define lita_candidaturas
    """
    db = current.db
    definir_tabla()
    carr_ids = [[c.carrera_id for c in i.candidatura_carrera.select()] for i in lita_candidaturas]
    # quitar duplicados y aplanar los resultados
    carreras_ids = list(set([item for sublist in carr_ids for item in sublist]))
    return carreras_ids

def obtenerCandidaturasPorCarrera(carrera_id,
        ano_academico_id=None,
        unidad_organica_id=None,
        prioridad=None,
        regimen_id=None):
    """Dado el ID de una carrera retorna la lista de candidaturas que han
       selecionado esa carrera
    """
    db = current.db
    definir_tabla()
    q = (db.candidatura.id > 0)
    if ano_academico_id:
        q &= (db.candidatura.ano_academico_id == ano_academico_id)
    if regimen_id:
        q &= (db.candidatura.regimen_unidad_organica_id == regimen_id)
    if unidad_organica_id:
        q &= (db.candidatura.unidad_organica_id == unidad_organica_id)
    else:
        if ano_academico_id:
            ac = db.ano_academico(ano_academico_id)
            q &= (db.candidatura.unidad_organica_id == ac.unidad_organica_id)
    q &= (db.candidatura.id == db.candidatura_carrera.candidatura_id)
    q &= (db.candidatura_carrera.carrera_id == carrera_id)
    if prioridad != None:
        q &= (db.candidatura_carrera.prioridad == prioridad)
    return db(q).select(db.candidatura.id, distinct=True)

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
    if not hasattr(db, 'candidatura_carrera'):
        db.define_table('candidatura_carrera',
            Field('candidatura_id', 'reference candidatura'),
            Field('carrera_id', 'reference carrera_uo'),
            Field('prioridad', 'integer', default=0),
            )
        db.candidatura_carrera.carrera_id.label = T('Carrera')
        db.candidatura_carrera.prioridad.label = T('Prioridad')
        db.commit()
