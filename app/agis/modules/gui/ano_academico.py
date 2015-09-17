# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import ano_academico as model
from applications.agis.modules import tools

__doc__ = "HTML para años académicos"

def seleccionar_ano(unidad_organica_id=None):
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    model.definir_tabla()
    q = (db.ano_academico.id > 0)
    if request.vars.unidad_organica_id:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    if unidad_organica_id:
        q &= (db.ano_academico.unidad_organica_id == unidad_organica_id)
    manejo = tools.selector(q,
        [db.ano_academico.nombre], 'ano_academico_id')
    return manejo
