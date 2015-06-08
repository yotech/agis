#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import provincia

def definir_tabla():
    db = current.db
    T = current.T
    provincia.definir_tabla()
    if not hasattr(db, 'municipio'):
        db.define_table('municipio',
            Field('codigo','string',length=2,required=True,notnull=True,
                label=T('Código'),comment=T('Código de 2 digitos'),),
            Field('nombre','string',length=80,required=True,
                unique=True,notnull=True,label=T('Nombre'),),
            Field('provincia_id', 'reference provincia',label=T('Provincia')),
            plural=T('Municipios'),
            singular=T('Municipio'),
            format='%(nombre)s',
        )
        db.municipio.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_MATCH('^\d\d$', error_message=T('No es un código valido')),
        ]
        db.municipio.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db, 'municipio.nombre'),
        ]
        db.municipio.provincia_id.requires = IS_IN_DB(db,'provincia.id',
            '%(nombre)s',
            zero=None,
        )
