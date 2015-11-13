#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import tipos_ensennanza as tipo_escuela
from agiscore.db import provincia
from agiscore.db import municipio


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
    condq = (db.escuela_media.tipo_escuela_media_id !=
             tipo_escuela.obtener_por_uuid(tipo_escuela.ID_PROTEGIDO).id)
    db.escuela_media.provincia_id.show_if = condq
    db.escuela_media.municipio_id.show_if = condq
    db.escuela_media.id.readable = False
    # esto debe mantenerse lo más proximo posible a la contrucción del GRID
    if ('new' in request.args) or ('edit' in request.args):
        if request.vars.tipo_escuela_media_id:
            # guardando el formulario
            sid = int(request.vars.tipo_escuela_media_id)
            pid = tipo_escuela.obtener_por_uuid(tipo_escuela.ID_PROTEGIDO).id
            if sid == pid: # si es el valor ID_PROTEGIDO
                # asignarle valores a la provincia y municipo
                id_p = db.provincia.obtener_por_uuid(provincia.ID_PROTEGIDO).id
                id_m = db.municipio.obtener_por_uuid(municipio.ID_PROTEGIDO).id
                request.vars.provincia_id = id_p
                request.vars.municipio_id = id_m
                request.post_vars.provincia_id = id_p
                request.post_vars.municipio_id = id_m
                db.escuela_media.provincia_id.default = id_p
                db.escuela_media.municipio_id.default = id_m
                db.escuela_media.municipio_id.requires = []
    manejo = SQLFORM.grid(db.escuela_media,
        showbuttontext=False, maxtextlength=100, details=False,
        csv=False,orderby=[db.escuela_media.nombre])
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
