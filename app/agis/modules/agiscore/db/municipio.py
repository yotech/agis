#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import provincia

ID_PROTEGIDO = 'd6d6ad5e-1dcd-4218-b548-8372aae07e49'

def obtener_por_uuid(uuid):
    definir_tabla()
    db = current.db
    return db(db.municipio.uuid==uuid).select().first()

def obtener(id=None, provincia_id=None):
    db = current.db
    if not hasattr(db, 'municipio'):
        definir_tabla()
    if id:
        return db.municipio[id]
    else:
        if provincia_id:
            query = ((db.municipio.id > 0) & (db.municipio.provincia_id == provincia_id))
            return db(query).select().first()
        else:
            return db.municipio[1]

def obtener_posibles(provincia_id):
    """Data una provincia retorna los posibles municipios es forma de SET para usar en IS_IN_SET"""
    municipios = obtener_municipios(provincia_id)
    pos = []
    for item in municipios:
        pos.append( (item.id, item.nombre) )
    return pos

def obtener_municipios(provincia_id):
    """retorna los municipios que pertenezcan a provincia"""
    db = current.db
    definir_tabla()
    return db(db.municipio.provincia_id == provincia_id).select(db.municipio.ALL)

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
            db.my_signature,
            plural=T('Municipios'),
            singular=T('Municipio'),
            format='%(nombre)s',
        )
        db.municipio.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_MATCH('^\d\d$', error_message=T('No es un código valido')),
        ]
        db.municipio.nombre.requires = [
            IS_UPPER(),
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db, 'municipio.nombre'),
        ]
        db.municipio.provincia_id.requires = IS_IN_DB(db,'provincia.id',
            '%(nombre)s',
            zero=None,
        )
        db.municipio.obtener_por_uuid = obtener_por_uuid
