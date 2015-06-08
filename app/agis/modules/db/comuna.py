#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import municipio

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
            format='%(nombre)s - %(municipio_id)s',
            plural=T('Comunas'),
            singular=T('Comuna'),
        )
        db.comuna.codigo.requires = [
            IS_NOT_EMPTY(error_message=T('Código es requerido')),
            IS_MATCH('^\d\d$', error_message=T('Código no es valido')),
        ]
        db.comuna.nombre.requires = [
            IS_NOT_EMPTY(error_message=T('Nombre es requerido')),
        ]
        db.comuna.municipio_id.requires = IS_IN_DB(db,'municipio.id',
            '%(nombre)s',
            zero=None,
            error_message=T('Debe seleccionar un municipio'),
        )
