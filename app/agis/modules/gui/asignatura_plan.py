# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools
from applications.agis.modules.db import asignatura_plan as model

__doc__ = "HTML auxiliar para asignatura_plan"

def seleccionar_asignatura(plan_id=None, no_esta_en=[]):
    """GRID de selección de asignaturas en algún plan"""
    request = current.request
    db = current.db
    model.definir_tabla()
    query = (db.asignatura_plan.id > 0)
    if plan_id:
        query &= (db.asignatura_plan.plan_curricular_id == plan_id)
    else:
        if request.vars.plan_curricular_id:
            plan_id = int(request.vars.plan_curricular_id)
            query &= (db.asignatura_plan.plan_curricular_id == plan_id)
    query &= (db.asignatura_plan.asignatura_id == db.asignatura.id)
    if no_esta_en:
        query &= (~db.asignatura_plan.asignatura_id.belongs(no_esta_en))
    return tools.selector(query,
        [db.asignatura_plan.asignatura_id],
        'asignatura_plan_id')
