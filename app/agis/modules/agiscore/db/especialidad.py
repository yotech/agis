# -*- coding: utf-8 -*-
from gluon import Field
from agiscore.db import carrera_uo
from gluon.validators import IS_NOT_EMPTY, IS_IN_DB, IS_UPPER

def definir_tabla(db, T):
    carrera_uo.definir_tabla()
    if not hasattr(db, 'especialidad'):
        tbl = db.define_table('especialidad',
            Field('abreviatura', 'string', length=4),
            Field('nombre', 'string', length=100),
            Field('carrera_id', 'reference carrera_uo'))
        tbl.abreviatura.label = T('Abreviatura')
        tbl.nombre.label = T('Nombre')
        tbl.carrera_id.label = T("Carrera")
        tbl.abreviatura.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        tbl.nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        tbl.carrera_id.requires = IS_IN_DB(db, db.carrera_uo.id, zero=None)