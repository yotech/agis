#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.tipo_documento_identidad.id.readable = False
    return tools.manejo_simple(db.tipo_documento_identidad, orden=[db.tipo_documento_identidad.nombre])

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'tipo_documento_identidad'):
        db.define_table('tipo_documento_identidad',
            Field('nombre','string',required=True,notnull=True,
                length=50,label=T('Nombre'),),
            format='%(nombre)s',
        )
        db.tipo_documento_identidad.nombre.requires = [
            IS_UPPER(),
            IS_NOT_EMPTY(),IS_NOT_IN_DB(db, 'tipo_documento_identidad.nombre'), ]
        db.commit()
