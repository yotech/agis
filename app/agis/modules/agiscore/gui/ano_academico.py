# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import ano_academico as model
from agiscore import tools

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
        db.ano_academico.unidad_organica_id.readable = False
        q &= (db.ano_academico.unidad_organica_id == unidad_organica_id)
    db.ano_academico.id.readable = False
    grid = tools.selector(q,
        [db.ano_academico.nombre], 'ano_academico_id')
    co = CAT()
    header = DIV(T("Seleccionar año académico"), _class="panel-heading")
    body = DIV(grid, _class="panel-body")
    co.append(DIV(header, body, _class="panel panel-default"))
    return co
