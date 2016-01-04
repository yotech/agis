#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import persona
from agiscore.db import departamento
from agiscore.db.profesor import profesor_grado_represent
from agiscore.db.profesor import profesor_vinculo_represent
from agiscore.db.profesor import PROFESOR_VINCULO_VALUES
from agiscore.db.profesor import PROFESOR_GRADO_VALUES
from agiscore.db.profesor import profesor_format

def copia_uuid_callback(valores):
    """Se llama antes de insertar un valor en la tabla

    En este caso lo estamos usando para copiar el UUID de la persona
    """
    db = current.db
    p = db.persona(valores['persona_id'])
    valores['uuid'] = p.uuid

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T
    persona.definir_tabla()
    departamento.definir_tabla()
    if not hasattr(db, 'funsionario'):
        tbl = db.define_table('funsionario',
            Field('persona_id', 'reference persona'),
            Field('vinculo', 'string', length=1),
            Field('grado', 'string', length=1),
            Field('fecha_entrada', 'date'),
            Field('departamento_id', 'reference departamento'),
            db.my_signature,
            format=profesor_format,
        )
        tbl.id.readable = False
        tbl._before_insert.append(copia_uuid_callback)
        tbl.persona_id.label = T('Nombre')
        tbl.persona_id.writable = False
        tbl.vinculo.label = T('Vinculo')
        tbl.vinculo.represent = profesor_vinculo_represent
        tbl.vinculo.requires = IS_IN_SET(PROFESOR_VINCULO_VALUES, zero=None)
        tbl.vinculo.default = '1'
        tbl.grado.label = T('Grado científico')
        tbl.grado.represent = profesor_grado_represent
        tbl.grado.requires = IS_IN_SET(PROFESOR_GRADO_VALUES, zero=None)
        tbl.grado.default = '2'
        tbl.fecha_entrada.label = T('Fecha entrada')
        tbl.fecha_entrada.comment = T('Fecha de entrada a la Unidad Organica')
        tbl.fecha_entrada.required = True
        tbl.fecha_entrada.requires.append(
            IS_NOT_EMPTY(error_message=current.T('Información requerida')),
            )
        tbl.departamento_id.label = T('Departamento')
        tbl.departamento_id.requires = IS_IN_DB(db, 'departamento.id', '%(nombre)s', zero=None)
