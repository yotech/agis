#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import *

def definir_tabla():
    db = current.db
    T = current.T
    
    if not hasattr(db, 'pais'):
        db.define_table('pais',
            Field('codigo','string', length=3),
            Field('nombre', 'string', length=30),
            format="%(nombre)s",
        )
        db.commit()
        db.pais.codigo.requires.append(IS_NOT_EMPTY())
        db.pais.codigo.requires.append(IS_MATCH('^\d{3,3}$', ))
        db.pais.codigo.requires.append(IS_NOT_IN_DB(db, 'pais.codigo'))
        db.pais.nombre.requires.append(IS_NOT_EMPTY())
        db.pais.nombre.requires.append(IS_UPPER())
        db.pais.nombre.requires.append(IS_NOT_IN_DB(db, 'pais.nombre'))
