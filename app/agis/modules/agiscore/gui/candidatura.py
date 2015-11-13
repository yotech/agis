# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import candidatura as model
from applications.agis.modules.gui.mic import *
from applications.agis.modules.gui.persona import leyenda_persona

__doc__ = """Herramientas de GUI para candidaturas"""

def leyenda_candidatura():
    T = current.T
    l = Leyenda()
    l.append(T('Documentos'),model.CANDIDATURA_DOCUMENTOS_VALUES)
    l.append(T('Estado'), model.CANDIDATURA_ESTADO)
    return l

def seleccionar_candidato(estado_candidatura = None,
                unidad_organica_id = None,
                ano_academico_id = None):
    """Retorna GRID para seleccionar un candidato"""
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    model.definir_tabla() # definir los modelos si no se ha hecho ya
    query = ((db.persona.id == db.estudiante.persona_id) &
             (db.candidatura.estudiante_id == db.estudiante.id))
    if estado_candidatura:
        query &= (db.candidatura.estado_candidatura == estado_candidatura)
    if unidad_organica_id:
        query &= (db.candidatura.unidad_organica_id == unidad_organica_id)
    if ano_academico_id:
        query &= (db.candidatura.ano_academico_id == ano_academico_id)
    m = tools.selector(query,
        [db.candidatura.id, db.persona.nombre_completo],
        'candidatura_id',
        'candidatura')
    leyenda = DIV(DIV(leyenda_persona(),_class="col-md-6"),
                  DIV(leyenda_candidatura(),_class="col-md-6"),
                  _class="row")
    m = DIV(DIV(m, _class="col-md-12"), _class="row")
    return CAT(leyenda, m)
