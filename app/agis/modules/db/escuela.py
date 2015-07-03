#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import region_academica

CLASIFICACIONES = {
            '10': 'Universidad',
            '20': 'Instituto superior',
            '21': 'Instituto superior politécnico',
            '30': 'Escuela superior',
            '31': 'Escuela superior técnica',
            '32': 'Escuela superior politécnica',
            '40': 'Academia',
            '70': 'Instituto de investigaciones',
        }
def clasficiacion_respresent(valor, registro):
    return current.T(CLASIFICACIONES[valor])

NATURALEZAS = {
            '1': 'Pública',
            '2': 'Privada',
            '3': 'Mixta',
        }
def naturaleza_represent(valor, registro):
    return current.T(NATURALEZAS[valor])

def calcular_codigo_escuela(r):
    """Dado un registro de Escuela calcula el código de la misma"""
    db = current.db
    ar = db.region_academica[r['region_academica_id']]
    return ar.codigo + r['clasificacion'] + r['naturaleza'] + r['codigo_registro']

def obtener_escuela(escuela_id=None):
    """retorna el registro de la escuela por defecto"""
    db = current.db
    definir_tabla()
    return db.escuela[1]

def obtener_region(escuela=None):
    """
    Retorna la región academica a la que pertenece la escuela
    """
    if not escuela:
        escuela = obtener_escuela()
    return region_academica.obtener_region(escuela.region_academica_id)

def obtener_sede_central(escuela=None):
    """Obtiene la Unidad Organica que representa la sede central para una escuela.
    Si no se da el parametro escuela se asume la escuela por defecto.
    """
    from applications.agis.modules.db import unidad_organica
    if not escuela:
        escuela=obtener_escuela()
    return unidad_organica.obtener_sede_central(escuela.id)

def definir_tabla():
    """Define la tabla Escuela"""
    db = current.db
    T = current.T
    region_academica.definir_tabla()
    if not hasattr(db, 'escuela'):
        db.define_table('escuela',
            Field('nombre','string',length=100,required=True,
                label=T('Nombre'),),
            Field('region_academica_id','reference region_academica',
                ondelete='SET NULL',label=T('Región Academica'),),
            Field('clasificacion','string',length=2,required=True,
                label=T('Clasificación'),),
            Field('naturaleza','string',length=1,required=True,
                label=T('Naturaleza'),),
            Field('codigo_registro','string',length=3,required=True,
                label=T('Código de registro'),
                comment=T(
                    '''Código de registro en el ministerio de educación'''
                )),
            Field('codigo',compute=calcular_codigo_escuela,
                notnull=True,label=T('Código'),),
            Field('logo','upload',required=False,notnull=False,autodelete=True,
                uploadseparate=True,label=T('Logo'),
            ),
            format='%(nombre)s',
            singular=T('Escuela'),
            plural=T('Escuelas'),
        )
        db.escuela.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db,'escuela.nombre',
                error_message=T('Ya existe en la BD'),
            )
        ]
        db.escuela.region_academica_id.requires = IS_IN_DB(db,'region_academica.id',
            '%(codigo)s - %(nombre)s',
            zero=T('Escoja uno:'),
            error_message=T('Escoja la región academica'),
        )
        db.escuela.logo.requires = IS_EMPTY_OR(IS_IMAGE())
        db.escuela.clasificacion.requires = IS_IN_SET(CLASIFICACIONES,zero=None)
        db.escuela.clasificacion.represent = clasficiacion_respresent
        db.escuela.naturaleza.requires = IS_IN_SET(NATURALEZAS,zero=None)
        db.escuela.naturaleza.represent = naturaleza_represent
        db.escuela.codigo_registro.requires = [
            IS_NOT_EMPTY(error_message=T('Código de registro es requerido')),
            IS_MATCH('^\d{3,3}$', error_message=T('No es válido')),
            IS_NOT_IN_DB(db,'escuela.codigo_registro'),
        ]
        db.commit()
