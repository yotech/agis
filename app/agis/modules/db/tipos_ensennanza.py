#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    db.tipo_escuela_media.id.readable = False
    return tools.manejo_simple(db.tipo_escuela_media, [db.tipo_escuela_media.codigo])

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'tipo_escuela_media'):
        db.define_table('tipo_escuela_media',
            Field('codigo','string',length=2,label=T('Código'),notnull=True,
                required=True,unique=True,comment=T('Código de dos digitos'),),
            Field('nombre','string',length=10,label=T('Nombre'),required=True,
                notnull=True,),
            format='%(nombre)s',
        )
        db.tipo_escuela_media.codigo.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{2,2}$'),
            IS_NOT_IN_DB(db,'tipo_escuela_media.codigo',)]
        db.tipo_escuela_media.nombre.requires = [ IS_NOT_EMPTY(),
            IS_NOT_IN_DB(db, 'tipo_escuela_media.nombre'),]
