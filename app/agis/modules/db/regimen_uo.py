#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import regimen

def obtener_posibles(unidad_organica_id):
    """
    Dada una unidad organica retorna el conjunto de regimenes que no estan asociados
    a esta.
    """
    definir_tabla()
    unidad_organica.definir_tabla()
    regimen.definir_tabla()
    db = current.db
    # esto es: dame todas las filas de "regimen" que no se han asociado a unidad_organica_id
    row = db(db.regimen_unidad_organica.unidad_organica_id == None).select(
        db.regimen.ALL, db.regimen_unidad_organica.ALL,
        left=db.regimen_unidad_organica.on((db.regimen.id == db.regimen_unidad_organica.regimen_id)
                                           &(db.regimen_unidad_organica.unidad_organica_id == unidad_organica_id)))
    pos = []
    for item in row:
        pos.append( (item.regimen.id, item.regimen.nombre) )
    return pos

def definir_tabla():
    db = current.db
    T = current.T
    if not hasattr(db, 'regimen_unidad_organica'):
        tbl = db.define_table('regimen_unidad_organica',
            Field('regimen_id','reference regimen', notnull=True),
            Field('unidad_organica_id','reference unidad_organica')
        )
        tbl.regimen_id.required=True
        tbl.unidad_organica_id.required=True
        tbl.regimen_id.label=T('Regímen')
        tbl.unidad_organica_id.label=T('Unidad organica')
        db.commit()
