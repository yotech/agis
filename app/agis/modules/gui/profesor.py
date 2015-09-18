# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.gui.mic import *
from applications.agis.modules.gui.persona import leyenda_persona
from applications.agis.modules.db import profesor as model

def form_editar_profesor(profesor_id):
    """Genera formulario de edición para profesor"""
    model.definir_tabla()
    db = current.db
    T = current.T
    p = db.profesor(profesor_id)
    title = H3(T("Datos del docente"))
    f = SQLFORM(db.profesor, p)
    c = CAT(title, DIV(DIV(f, _class="panel-body"),
               _class="panel panel-default"))
    return (c, f)

def leyenda_profesor():
    T = current.T
    l = Leyenda()
    l.append(T('Vinculo'), model.PROFESOR_VINCULO_VALUES)
    l.append(T('Categoría docente'), model.PROFESOR_CATEGORIA_VALUES)
    l.append(T('Grado científico'), model.PROFESOR_GRADO_VALUES)
    co = DIV(DIV(leyenda_persona(),_class="col-md-6"),
             DIV(l,_class="col-md-6"),
             _class="row")
    return co


def seleccionar_profesor(departamento = None):
    db = current.db
    query = model.obtener_profesores(dpto=departamento)
    return tools.selector(query,
        [db.profesor.grado, db.persona.nombre_completo],
        'profesor_id', tabla='profesor')
