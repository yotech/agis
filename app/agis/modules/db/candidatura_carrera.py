#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import carrera_uo

def definir_tabla():
    db = current.db
    T = current.T
    candidatura.definir_tabla()
    carrera_uo.definir_tabla()
    if not hasattr( db, 'candidatura_carrera' ):
        db.define_table( 'candidatura_carrera',
            Field( 'candidatura_id','reference candidatura' ),
            Field( 'carrera_id','reference carrera_uo' ),
            Field( 'prioridad','integer',default=0 ),
            )
        db.commit()
