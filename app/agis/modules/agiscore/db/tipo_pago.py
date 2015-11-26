#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools

# PERIOSIDAD_VALUES = {
#     '1':'ÚNICA',
# }
# def periosidad_represent(valor, fila):
#     T = current.T
#     return T(PERIOSIDAD_VALUES[valor])

def obtener_manejo():
    definir_tabla()
    db = current.db
    db.tipo_pago.id.readable = False
    db.tipo_pago.nombre.writable = False
    return tools.manejo_simple(db.tipo_pago, borrar=False, crear=False)

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'tipo_pago'):
        db.define_table('tipo_pago',
            Field('nombre', 'string', length=20),
#             Field( 'periosidad','string',length=1 ),
            Field('cantidad', 'double'),
            Field('activo', 'boolean', default=True),
            format="%(nombre)s",
            )
        db.tipo_pago.nombre.required = True
        db.tipo_pago.nombre.unique = True
        db.tipo_pago.nombre.requires = [IS_NOT_EMPTY()]
        db.tipo_pago.nombre.requires.append(IS_UPPER())
        db.tipo_pago.nombre.requires.append(
            IS_NOT_IN_DB(db, 'tipo_pago.nombre', error_message=T('Ya existe'))
        )
        db.tipo_pago.nombre.label = T('Nombre')
#         db.tipo_pago.periosidad.requires = IS_IN_SET( PERIOSIDAD_VALUES,zero=None )
#         db.tipo_pago.periosidad.default = '1'
#         db.tipo_pago.periosidad.label = T( 'Periosidad' )
#         db.tipo_pago.periosidad.represent=periosidad_represent
        db.tipo_pago.cantidad.label = T('Cantidad')
        db.tipo_pago.cantidad.default = 0.0
        db.tipo_pago.cantidad.required = True
        db.tipo_pago.activo.label = T('¿Activo?')
        db.commit()
