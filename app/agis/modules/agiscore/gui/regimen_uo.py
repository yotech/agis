# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools
from agiscore.gui.mic import *
from agiscore.db import regimen_uo as model

def seleccionar_regimen(unidad_organica_id):
    db = current.db
    T = current.T
    model.definir_tabla()
    q = (db.regimen_unidad_organica.id > 0)
    q &= (db.regimen_unidad_organica.unidad_organica_id == unidad_organica_id)
    grid = tools.selector(q,
        [db.regimen_unidad_organica.regimen_id], 'regimen_unidad_organica_id')
    co = CAT()
    header = DIV(T("Seleccionar año académico"), _class="panel-heading")
    body = DIV(grid, _class="panel-body")
    co.append(DIV(header, body, _class="panel panel-default"))
    return co
