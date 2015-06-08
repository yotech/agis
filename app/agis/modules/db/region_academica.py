#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def obtener_provincias(region):
    """
    Dada una región academica retornar el conjunto de las provincias que la conforman
    """
    db = current.db
    query = ((db.provincia.id > 0) & (db.provincia.region_academica_id == region.id))
    return db(query).select()

def obtener_region(region_id):
    """retorna el registro de región academica para la region region_id"""
    return current.db.region_academica[region_id]

def obtener_manejo():
    db = current.db
    T = current.T
    definir_tabla()
    db.region_academica.id.readable = False
    db.region_academica.id.writable = False
    manejo = tools.manejo_simple(
        db.region_academica, [db.region_academica.codigo]
    )

    return manejo

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'region_academica'):
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
        db.commit()
