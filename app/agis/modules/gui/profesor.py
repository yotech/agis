# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules.db import profesor as profesor_model

def form_editar_profesor(profesor_id):
    """Genera formulario de edición para profesor"""
    profesor_model.definir_tabla()
    db = current.db
    T = current.T
    p = db.profesor(profesor_id)
    title = H3(T("Datos del docente"))
    f = SQLFORM(db.profesor, p)
    c = CAT(title, DIV(DIV(f, _class="panel-body"),
               _class="panel panel-default"))
    return (c, f)
