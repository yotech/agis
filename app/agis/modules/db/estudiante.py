#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import persona

def estudiante_format(registro):
    db = current.db
    definir_tabla()
    return db.persona[registro.persona_id].nombre_completo

def definir_tabla():
    db = current.db
    T = current.T
    persona.definir_tabla()
    if not hasattr( db,'estudiante' ):
        db.define_table( 'estudiante',
            Field( 'persona_id', 'reference persona' ),
            format=estudiante_format,
            )
        db.commit()
