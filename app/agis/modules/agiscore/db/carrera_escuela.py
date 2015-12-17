# -*- coding: utf-8 -*-
from gluon import Field, IS_NOT_EMPTY, IS_MATCH
from gluon import current
from agiscore.db import escuela
from agiscore.db import descripcion_carrera
from gluon.validators import IS_NOT_IN_DB

def carreras_posibles(db):
    tbl = db.carrera_escuela
    estan_query  = (tbl.id > 0)
    estan_query &= (tbl.descripcion_id)
    estan_rows = db(estan_query).select(tbl.descripcion_id)
    estan = [r.descripcion_id for r in estan_rows]
    no_estan_query  = (db.descripcion_carrera.id > 0)
    no_estan_query &= (~db.descripcion_carrera.id.belongs(estan))
    no_estan_rows = db(no_estan_query).select(orderby=db.descripcion_carrera.nombre)
    posibles = [(r.id, r.nombre) for r in no_estan_rows]
    
    return posibles

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
        tbl.codigo.requires.append(IS_NOT_IN_DB(db, 'carrera_escuela.codigo'))
