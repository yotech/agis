#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools

def calcular_codigo(r):
    return r['codigo_mes'] + r['codigo_pnfq'] + r['codigo_unesco'] + r['codigo_carrera']

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.descripcion_carrera.id.readable = False
    db.descripcion_carrera.id.writable = False
    return tools.manejo_simple( db.descripcion_carrera,orden=[db.descripcion_carrera.nombre,] )

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'descripcion_carrera'):
        db.define_table('descripcion_carrera',
            Field('nombre','string',length=100,label=T('Nombre'),notnull=True,required=True),
            Field('codigo_mes','string',length=1,label='MES',notnull=True,required=True,
                comment=T('Código de un digito'),),
            Field('codigo_pnfq', 'string',length=2,label='PNFQ',notnull=True,required=True,
                comment=T('Código de dos digitos')),
            Field('codigo_unesco','string',length=3,label='UNESCO',notnull=True,required=True,
                comment=T('Código de tres digitos')),
            Field('codigo_carrera','string',length=3,notnull=True,required=True,
                comment=T('Código de tres digitos'),
                label=T('Código de carrera'),),
            Field('codigo', 'string',length=9,label=T('Código'),notnull=True,required=False,unique=True,
                compute=calcular_codigo,),
            format='%(nombre)s',
            singular=T('Descripción de Carrera'),
            plural=T('Descripciones de carreras'),
        )
        db.descripcion_carrera.codigo_mes.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{1,1}$',) ]
        db.descripcion_carrera.codigo_pnfq.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{2,2}$') ]
        db.descripcion_carrera.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
            IS_NOT_IN_DB(db,'descripcion_carrera.nombre')]
        db.descripcion_carrera.codigo_unesco.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{3,3}$', ), ]
        db.descripcion_carrera.codigo_carrera.requires = [ IS_NOT_EMPTY(),IS_MATCH('^\d{3,3}$'), ]
