#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import persona

def estudiante_format(registro):
    db = current.db
    definir_tabla()
    return db.persona[registro.persona_id].nombre_completo

def obtener_persona(estudiante_id):
    """Dado un ID de estudiante retorna el registro de la persona asociada"""
    db = current.db
    definir_tabla()
    est = db.estudiante[estudiante_id]
    return db.persona[est.persona_id]

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
