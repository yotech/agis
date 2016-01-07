#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools

ID_PROTEGIDO = 'a57d6b2b-8f0e-4962-a2a6-95f5c82e015d'

def obtener_manejo(enlaces=[]):
    db = current.db
    db.tipo_escuela_media.id.readable = False
    return tools.manejo_simple(
        db.tipo_escuela_media, [db.tipo_escuela_media.codigo], borrar=False,
        enlaces=enlaces, editable=False
        )

def obtener_por_uuid(uuid):
    definir_tabla()
    db = current.db
    return db(db.tipo_escuela_media.uuid==uuid).select().first()

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'tipo_escuela_media'):
        db.define_table('tipo_escuela_media',
            Field('codigo','string',length=2,label=T('Código'),notnull=True,
                required=True,unique=True,comment=T('Código de dos digitos'),),
            Field('nombre','string',length=100,label=T('Nombre'),required=True,
                notnull=True,),
            db.my_signature,
            format='%(nombre)s',
        )
        db.tipo_escuela_media.id.readable = False
        db.tipo_escuela_media.id.writable = False
        db.tipo_escuela_media.codigo.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{2,2}$'),
            IS_NOT_IN_DB(db,'tipo_escuela_media.codigo',)]
        db.tipo_escuela_media.nombre.requires = [ IS_NOT_EMPTY(), IS_UPPER(),
            IS_NOT_IN_DB(db, 'tipo_escuela_media.nombre'),]
        db.tipo_escuela_media.obtener_por_uuid = obtener_por_uuid
