#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def obtener_manejo():
    db = current.db
    db.regimen.id.readable = False
    return tools.manejo_simple(db.regimen, [db.regimen.codigo],)

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'regimen'):
        db.define_table('regimen',
            Field('codigo','string',length=1,required=True,label=T('Código'),unique=True,),
            Field('nombre','string',length=50,required=True,label=T('Nombre'),),
            Field('abreviatura','string',length=1,required=True,requires=IS_NOT_EMPTY(),
                label=T('Abreviatura'),),
            format='%(nombre)s',
            singular=T('Régimen'),
            plural=T('Regímenes'),
        )
        db.regimen.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_NOT_IN_DB(db, 'regimen.codigo',
                error_message=T('Ya existe en la base de datos'),
            )
        ]
        db.regimen.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db, 'regimen.nombre',
                error_message=T('Ya existe en la base de datos'),
            )
        ]
        db.regimen.abreviatura.requires = IS_NOT_EMPTY(
            error_message=T('Abreviatura es requerido')
        )
