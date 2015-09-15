#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import persona

def estudiante_format(registro):
    db = current.db
    definir_tabla()
    return db.persona[registro.persona_id].nombre_completo

def obtener_por_persona(persona_id):
    db = current.db
    definir_tabla()
    p = db.persona(persona_id)
    if not p:
        return None
    return p.estudiante.select().first()

def esconder_campos():
    visibilidad(False)
def mostrar_campos():
    visibilidad(True)

def visibilidad(valor):
    """Cambia la propiedad readable de todos los campos de estudiante"""
    db = current.db
    definir_tabla()
    for f in db.estudiante:
        f.readable = False

def obtener_persona(estudiante_id):
    """Dado un ID de estudiante retorna el registro de la persona asociada"""
    db = current.db
    definir_tabla()
    est = db.estudiante[estudiante_id]
    return db.persona[est.persona_id]

def copia_uuid_callback(valores):
    """Se llama antes de insertar un valor en la tabla

    En este caso lo estamos usando para copiar el UUID de la persona
    """
    db = current.db
    p = db.persona(valores['persona_id'])
    valores['uuid'] = p.uuid

def definir_tabla():
    db = current.db
    T = current.T
    persona.definir_tabla()
    if not hasattr( db,'estudiante' ):
        db.define_table( 'estudiante',
            Field( 'persona_id', 'reference persona' ),
            db.my_signature,
            format=estudiante_format,
            )
        db.estudiante._before_insert.append(copia_uuid_callback)
        db.commit()
