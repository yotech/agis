#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import tipos_ensennanza as tipo_escuela
from applications.agis.modules.db import provincia
from applications.agis.modules.db import municipio


def obtener_escuelas(tipo_escuela_media_id):
    """Retorna las escuelas medias asociadas a un tipo si es que exite alguna"""
    definir_tabla()
    db = current.db
    return db( (db.escuela_media.id > 0) & (db.escuela_media.tipo_escuela_media_id == tipo_escuela_media_id) ).select()

def obtener_posibles(tipo_escuela_media_id):
    """retorna el conjunto de escuelas medias que correspondan a tipo_escuela_media_id"""
    escuelas = obtener_escuelas( tipo_escuela_media_id )
    op = []
    for e in escuelas:
        op.append( (e.id, e.nombre) )
    return op


def obtener_manejo():
    db = current.db
    request = current.request
    #if not hasattr(db, 'escuela_media'):
        #definir_tabla()

    if 'new' in request.args:
        #preparar el formulario para agregar un elemento.
        if request.vars.provincia_id:
            prov = provincia.obtener(int(request.vars.provincia_id))
        else:
            prov = provincia.obtener() # obtener cualquier provincia
        mun = municipio.obtener(provincia_id=prov.id)
        db.escuela_media.provincia_id.default = prov.id
        db.escuela_media.municipio_id.default = mun.id
        db.escuela_media.municipio_id.requires = IS_IN_DB(
            db(db.municipio.provincia_id == prov.id),
            'municipio.id',"%(nombre)s",zero=None
        )
    db.escuela_media.id.readable = False
    manejo = SQLFORM.grid(db.escuela_media,
        showbuttontext=False, maxtextlength=100, details=False,
        csv=False,orderby=[db.escuela_media.nombre], formstyle='bootstrap',
        )
    return manejo


def definir_tabla():
    db = current.db
    T = current.T
    tipo_escuela.definir_tabla()
    provincia.definir_tabla()
    municipio.definir_tabla()
    if not hasattr(db, 'escuela_media'):
        db.define_table('escuela_media',
            Field('codigo','string',length=4,label=T('Código'),required=True,notnull=True,),
            Field('nombre','string',length=100,label=T('Nombre'),required=True,notnull=True,),
            Field('tipo_escuela_media_id', 'reference tipo_escuela_media',label=T('Tipo de enseñanza media')),
            Field('provincia_id', 'reference provincia',label=T('Provincia')),
            Field('municipio_id', 'reference municipio',label=T('Municipio')),
            format="%(nombre)s",
        )
        db.escuela_media.codigo.requires = [
            IS_NOT_EMPTY(),IS_MATCH('^\d{4,4}$'),IS_NOT_IN_DB(db,'escuela_media.codigo'),
        ]
        db.escuela_media.nombre.requires = [
            IS_UPPER(),
            IS_NOT_EMPTY(),IS_NOT_IN_DB(db, 'escuela_media.nombre'),
        ]
        db.escuela_media.tipo_escuela_media_id.requires = IS_IN_DB(db,'tipo_escuela_media.id',
            '%(nombre)s',
            zero=None,
        )
