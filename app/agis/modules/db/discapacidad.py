#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.discapacidad.id.readable = False
    return tools.manejo_simple(db.discapacidad, orden=[db.discapacidad.codigo])

def definir_tabla():
    db = current.db
    T = current.T
    request = current.request
    if not hasattr(db,'discapacidad'):
        db.define_table('discapacidad',
            Field('codigo','string',length=1,unique=True,required=True,label=T('Código'),),
            Field('nombre','string',length=50,required=True,label=T('Nombre'),),
            format='%(nombre)s',
            plural=T('Tipos de discapacidades'),
            singular=T('Discapacidad'),
        )
        db.discapacidad.codigo.requires = [IS_NOT_EMPTY(),
            IS_MATCH('^\d{1,1}$'), IS_NOT_IN_DB(db,'discapacidad.codigo',)]
        db.discapacidad.nombre.requires = IS_NOT_EMPTY()
        db.commit()
