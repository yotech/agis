# -*- coding: utf-8 -*-
from gluon import Field, IS_NOT_EMPTY, IS_MATCH
from gluon import current
from agiscore.db import escuela
from agiscore.db import descripcion_carrera

def carrera_escuela_format(row):
    db = current.db
    desp = db.descripcion_carrera(row.descripcion_id)
    return desp.nombre

def definir_tabla(db, T):
    # TODO: fixme
    escuela.definir_tabla()
    descripcion_carrera.definir_tabla()
    if not hasattr(db, 'carrera_escuela'):
        tbl = db.define_table('carrera_escuela',
            Field('descripcion_id', 'reference descripcion_carrera'),
            Field('codigo', 'string', length=2),
            format=carrera_escuela_format)
        tbl.descripcion_id.label = T("Descripción de la carrera")
        tbl.codigo.label = T("Código IES")
        tbl.codigo.requires = [IS_NOT_EMPTY(), IS_MATCH('^\d{2,2}$')]
