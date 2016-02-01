# -*- coding: utf-8 -*-
from gluon import current
from gluon import Field
from gluon.validators import IS_NOT_EMPTY, IS_UPPER

from agiscore.db import unidad_organica

def _row_format(row):
    return ""

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T
    
    unidad_organica.definir_tabla()
    if not hasattr(db, 'turma'):
        tbl = db.define_table('turma',
            Field('nombre', 'string', length=50),
            Field('carrera_id', 'reference carrera_uo'),
            Field('regimen_id', 'reference regimen_unidad_organica'),
            Field('nivel_id', 'reference nivel_academico'),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format="%(nombre)s",
            )
        
        tbl.nombre.label = T('Nombre')
        tbl.nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        
        tbl.carrera_id.label = T("Carrera")
        tbl.regimen_id.label = T("Regímen")
        tbl.nivel_id.label = T("N. Académico")