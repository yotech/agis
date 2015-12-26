#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.asignatura.id.readable = False
    return tools.manejo_simple(db.asignatura)


def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'asignatura'):
        tbl = db.define_table('asignatura',
            Field('abreviatura', 'string', length=4),
            Field('nombre', 'string', length=50),
            format="%(abreviatura)s - %(nombre)s"
            )
        tbl.abreviatura.label = T('Abreviatura')
        tbl.abreviatura.requires = [IS_NOT_EMPTY(),
                                    IS_UPPER(),
                                    IS_NOT_IN_DB(db, 'asignatura.abreviatura')]
        tbl.abreviatura.comment = T('''
            Cuatro caracteres como máximo. Debe ser único
        ''')
        tbl.nombre.label = T('Nombre')
        tbl.nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
