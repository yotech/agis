#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from agiscore.db import unidad_organica
from agiscore.db import regimen

def obtener_regimenes_por_unidad(unidad_organica_id):
    definir_tabla()
    db = current.db
    return db( (db.regimen_unidad_organica.unidad_organica_id == unidad_organica_id) &
       (db.regimen_unidad_organica.regimen_id == db.regimen.id)
    ).select( db.regimen.nombre,db.regimen_unidad_organica.id )

def obtener_regimenes( unidad_organica_id ):
    definir_tabla()
    db = current.db
    resultados = db( (db.regimen_unidad_organica.unidad_organica_id == unidad_organica_id) &
       (db.regimen_unidad_organica.regimen_id == db.regimen.id)
    ).select( db.regimen.ALL, db.regimen_unidad_organica.ALL )
    p = []
    for r in resultados:
        p.append( (r.regimen_unidad_organica.id,r.regimen.nombre) )
    return p

def obtener_posibles_en_instituto(unidad_organica_id):
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

def regimen_unidad_organica_format(registro):
    #definir_tabla()
    return current.db.regimen[registro.regimen_id].nombre

def definir_tabla():
    db = current.db
    T = current.T
    regimen.definir_tabla()
    unidad_organica.definir_tabla()
    if not hasattr(db, 'regimen_unidad_organica'):
        tbl = db.define_table('regimen_unidad_organica',
            Field('regimen_id','reference regimen', notnull=True),
            Field('unidad_organica_id','reference unidad_organica'),
            format=regimen_unidad_organica_format
        )
        tbl.regimen_id.required=True
        tbl.unidad_organica_id.required=True
        tbl.regimen_id.label=T('Regímen')
        tbl.unidad_organica_id.label=T('Unidad organica')
        db.commit()
