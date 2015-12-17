#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools
from agiscore.db import unidad_organica

NIVEL_VALORES = [
    (0, current.T('ACCESO')),
    (1, current.T('1RO')),
    (2, current.T('2DO')),
    (3, current.T('3RO')),
    (4, current.T('4TO')),
    (5, current.T('5TO')),
    (6, current.T('6TO')),
    (7, current.T('FINALISTA')),
]

ACCESO = 0

def nivel_represent(v, fila):
    valores = {0: 'ACCESO',
               1: '1RO',
               2: '2DO',
               3: '3RO',
               4: '4TO',
               5: '5TO',
               6: '6TO',
               7: 'FINALISTA'}
    T = current.T
    return T(valores[v])

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.nivel_academico.id.readable = False
    return tools.manejo_simple(db.nivel_academico)

def actualizar_niveles(niveles, unidad_organica_id):
    """Actualiza los niveles académicos disponibles para la UO"""
    db = current.db
    # eliminar de los que estan los que no se seleccionaron
    db(~db.nivel_academico.nivel.belongs(niveles)).delete()
    db.commit()
    # agregar los nuevos seleccionados
    for n in niveles:
        db.nivel_academico.update_or_insert(
            nivel=n,
            unidad_organica_id=unidad_organica_id
        )
    db.commit()

def obtener_nivel(nivel, unidad_organica_id):
    db = current.db
    definir_tabla()
    return db((db.nivel_academico.nivel == nivel) & 
        (db.nivel_academico.unidad_organica_id == unidad_organica_id)).select()

def obtener_niveles(unidad_organica_id):
    """Dada una UO retorna los niveles que tiene la misma"""
    db = current.db
    definir_tabla()
    q = (db.nivel_academico.unidad_organica_id == unidad_organica_id)
    return db(q).select(db.nivel_academico.ALL)

def nivel_academico_format(fila):
    return nivel_represent(fila.nivel, None)

def definir_tabla():
    db = current.db
    T = current.T

    unidad_organica.definir_tabla()
    if not hasattr(db, 'nivel_academico'):
        db.define_table('nivel_academico',
            Field('nivel', 'integer', default=0),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format=nivel_academico_format,
        )
        db.nivel_academico.nivel.label = T('Nivel')
        db.nivel_academico.nivel.requires = IS_IN_SET(NIVEL_VALORES, zero=None)
        db.nivel_academico.nivel.represent = nivel_represent
        db.nivel_academico.unidad_organica_id.label = T('Unidad Orgánica')
        db.commit()
