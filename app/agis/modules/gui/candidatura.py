# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import candidatura as model

__doc__ = """Herramientas de GUI para candidaturas"""

def seleccionar_candidato(context,
                estado_candidatura = '1',
                unidad_organica = None,
                ano_academico = None):
    """Muestra GRID para seleccionar un evento"""
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    model.definir_tabla() # definir los modelos si no se ha hecho ya
    query = ((db.persona.id == db.estudiante.persona_id) &
             (db.candidatura.estudiante_id == db.estudiante.id))
    query &= (db.candidatura.estado_candidatura == estado_candidatura)
    if unidad_organica:
        query &= (db.candidatura.unidad_organica_id == unidad_organica.id)
    if ano_academico:
        query &= (db.candidatura.ano_academico_id == ano_academico.id)
    context.manejo = tools.selector(query,
        [db.candidatura.id, db.persona.nombre_completo],
        'candidatura_id',
        'candidatura')
    return context
