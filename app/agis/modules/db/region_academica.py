#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def definir_tabla():
    db = current.db
    T = current.T
    db.define_table('region_academica',
        Field('nombre', 'string',
            length=50,
            required=True,
            notnull=True,
            label=T('Nombre'),
        ),
        Field('codigo','string',
            length=2,
            required=True,
            notnull=True,
            unique=True,
            label=T('Código'),
            comment=T('Código de dos dígitos'),
        ),
        format='%(nombre)s - %(codigo)s',
        singular=T('Region academica'),
        plural=T('Regiones academicas'),
    )
    db.region_academica.nombre.requires = [
        IS_NOT_EMPTY(error_message=T('El nombre es requerido')),
        IS_NOT_IN_DB(db,'region_academica.nombre',
            error_message=T('Ya existe ese nombre en la BD'),
        ),
    ]
    db.region_academica.codigo.requires = [
        IS_NOT_EMPTY(error_message=T('El código es requerido')),
        IS_MATCH('^\d{2,2}$', error_message = T('Código no es valido')),
        IS_NOT_IN_DB(db,'region_academica.codigo',
            error_message=T('Ya existe una región academica con ese código'),
        ),
    ]
