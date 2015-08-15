#!/usr/bin/env python
# -*- coding: utf-8 -*-
import region_academica
from gluon import *

ID_PROTEGIDO = '4a9f5199-aae6-4cdc-8c00-080b0bc19c0b'

def obtener(id=None):
    db = current.db
    if not id:
        id = 1
    if not hasattr(db, 'provincia'):
        definir_tabla()
    return db.provincia[id]

def definir_tabla():
    """Define la tabla provincia"""
    db = current.db
    T = current.T
    region_academica.definir_tabla() # pre-requisito
    if not hasattr(db, 'provincia'):
        db.define_table('provincia',
            Field('codigo','string',
                length=2,
                unique=True,
                required=True,
                label=T('Código'),
                comment=T("Código de 2 digitos"),
            ),
            Field('nombre','string',
                length=50,
                required=True,
                notnull=True,
                label=T('Nombre'),
            ),
            Field('region_academica_id', 'reference region_academica',
                ondelete='SET NULL',
                label=T('Región academica'),
            ),
            db.my_signature,
            format='%(nombre)s',
            singular=T('Provincia'),
            plural=T('Provincias'),
        )
        db.provincia.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_NOT_IN_DB(db, 'provincia.codigo',
                error_message=T('Ya existe ese código en la BD')
            ),
        ]
        db.provincia.nombre.requires = [
            IS_UPPER(),
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db, 'provincia.nombre',
                error_message=T('Ya existe una provicia con ese nombre en la BD'),
            ),
        ]
        db.provincia.region_academica_id.requires = IS_IN_DB(db, 'region_academica.id',
            '%(codigo)s - %(nombre)s',
            zero=None,
        )
        db.commit()
