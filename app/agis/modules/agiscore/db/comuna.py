#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import municipio

ID_PROTEGIDO = '4b4fb0f3-c30c-4fa0-9840-477ab51a4478'

def obtener_posibles(municipio_id):
    comunas = obtener_comunas( municipio_id )
    op = []
    for c in comunas:
        op.append( (c.id,c.nombre) )
    return op

def obtener_comunas(municipio_id):
    """Dado un municipio retorna las comunas que perteneces a este"""
    definir_tabla()
    db = current.db
    return db( (db.comuna.id > 0) & ( db.comuna.municipio_id == municipio_id ) ).select()

def definir_tabla():
    db = current.db
    T = current.T
    municipio.definir_tabla()
    if not hasattr(db, 'comuna'):
        db.define_table('comuna',
            Field('codigo','string',length=2,label=T('Código'),
                required=True,notnull=True,),
            Field('nombre','string',length=80,label=T('Nombre'),
                required=True,notnull=True,),
            Field('municipio_id','reference municipio',required=True,
                label=T('Municipio'),),
            db.my_signature,
            format='%(nombre)s',
            plural=T('Comunas'),
            singular=T('Comuna'),
        )
        db.comuna.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_MATCH('^\d\d$', error_message=T('Código no es valido')),
        ]
        db.comuna.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_UPPER()
        ]
        db.comuna.municipio_id.requires = IS_IN_DB(db,'municipio.id',
            '%(nombre)s',
            zero=None,
            error_message=T('Debe seleccionar un municipio'),
        )
