#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Describe la asignación de las aulas a los estudiantes al realizar un examen
"""

from gluon import *
from agiscore.db import aula
from agiscore.db import examen
from agiscore.db import estudiante
from agiscore.db import candidatura

def buscar_aula_dispobible(examen_id):
    """Dado un examen retorna un aula que no este llena para el examen"""
    db = current.db
    ex = db.examen(examen_id)
    aulas = examen.obtener_aulas(ex.id)
    for a in aulas:
        if not esta_llena(ex.id, a.id):
            return a
    return None

def esta_llena(examen_id, aula_id):
    """Retorna True si todos los puestos para el examen han sido asignados"""
    db = current.db
    ex = db.examen(examen_id)
    au = db.aula(aula_id)
    assert (ex != None) and (au != None)
    asignados = db((db.examen_aula_estudiante.examen_id == ex.id) &
       (db.examen_aula_estudiante.aula_id == au.id)
      ).count()
    return (asignados >= au.capacidad)

def distribuir_candidaturas(examen_id):
    """Distribuye candidatos por aulas para examen de acceso"""
    db = current.db
    ex = db.examen(examen_id)
    assert ex is not None
    # eliminar cualquier asignación anterior para ese examen
    db(db.examen_aula_estudiante.examen_id == examen_id).delete()
    db.commit()
    # buscar todos los estudiantes que deben realizar el examen
    cand_ids = examen.obtener_candidaturas(ex.id) # candidaturas, hay que convertirlos en estudiantes
    estudiantes = [(db.candidatura(c.id)).estudiante_id for c in cand_ids]
    # buscar las aulas definidas para el examen
    aulas = examen.obtener_aulas(ex.id)
    # comprobar que los espacios disponibles en las aulas sean los suficientes
    # para acomodar a los estudiantes.
    total = aula.capacidad_total(aulas)
    if len(estudiantes) <= total:
        """asignarle las aulas a los estudianes"""
        for est in estudiantes:
            aula_disponible = buscar_aula_dispobible(examen_id)
            if aula_disponible:
                db.examen_aula_estudiante.insert(
                    examen_id = ex.id,
                    aula_id = aula_disponible.id,
                    estudiante_id = est.id
                    )
                db.commit()

def distribuir_estudiantes(examen_id):
    """Dado un examen intenda distribuir los estudiantes que deben realizar el mismo
    en las aulas asignadas para el examen.
    """
    db = current.db
    examen = db.examen(examen_id)
    assert examen != None
    if examen.tipo == '1':
        # distrubuir candidaturas por aulas
        distribuir_candidaturas(examen_id)
    # TODO: agregar condicionales para el resto de los tipos de examen.

def estudiante_id_represent(v, row):
    db = current.db
    return db.estudiante._format(db.estudiante(v))

def definir_tabla():
    db = current.db
    T = current.T
    aula.definir_tabla()
    examen.definir_tabla()
    estudiante.definir_tabla()
    if not hasattr(db, 'examen_aula_estudiante'):
        db.define_table('examen_aula_estudiante',
            Field('estudiante_id','reference estudiante'),
            Field('examen_id','reference examen'),
            Field('aula_id','reference aula'),
        )
        db.examen_aula_estudiante.estudiante_id.label = T('Estudiante')
        db.examen_aula_estudiante.estudiante_id.represent = estudiante_id_represent
        db.examen_aula_estudiante.examen_id.label = T('Examen')
        db.examen_aula_estudiante.aula_id.label = T('Aula')
        db.commit()
