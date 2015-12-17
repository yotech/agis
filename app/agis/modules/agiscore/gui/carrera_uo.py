# -*- coding: utf-8 -*-
from gluon import current
# from gluon.storage import Storage
# from agiscore import tools
# from agiscore.gui.mic import grid_simple
# from agiscore.db import carrera_uo as model
# from gluon.validators import IS_IN_SET


# def grid_carreras_uo(unidad, db, T,
#                      request=None,
#                      auth=None,
#                      conf=None):
#     request = current.request if request is None else request
#     auth = current.auth if auth is None else auth
#     conf = current.conf if conf is None else conf
#     
#     tbl = db.carrera_uo
#         
#     query = (tbl.id > 0)
#     query &= (tbl.unidad_organica_id == unidad.id)
#     
#     puede_crear = auth.has_membership(role=conf.take('roles.admin'))
#     puede_editar, puede_borrar = (puede_crear, puede_crear)
#     
#     tbl.unidad_organica_id.writable = False
#     tbl.carrera_escuela_id.label = T("Carrera")
#     
#     if 'new' in request.args:
#         tbl.unidad_organica_id.default = unidad.id
#         posibles = model.obtener_posibles(db, unidad.id)
#         tbl.carrera_escuela_id.requires = IS_IN_SET(posibles, zero=None)
#     
#     campos = [tbl.carrera_escuela_id]
#     text_length = {'carrera_uo.carrera_escuela_id': 60}
#     
#     grid = grid_simple(query,
#                        fields=campos,
#                        searchable=False,
#                        editable=puede_editar,
#                        create=puede_crear,
#                        deletable=puede_borrar,
#                        maxtextlengths=text_length,
#                        args=request.args[:1])
#     
#     return grid

def seleccionar_carrera(unidad_organica_id=None):
    """Genera un GRID para la selección de una carrera"""
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    # context.asunto = T('Seleccione la carrera')
    query = (db.carrera_uo.id > 0)
    if unidad_organica_id:
        query &= (db.carrera_uo.unidad_organica_id == unidad_organica_id)
    query &= (db.carrera_uo.carrera_escuela_id == db.carrera_escuela.id)
    query &= (db.carrera_escuela.descripcion_id == db.descripcion_carrera.id)
    c = tools.selector(query,
        [db.carrera_uo.id, db.descripcion_carrera.nombre],
        'carrera_uo_id', tabla='carrera_uo')
    # response.title = context.unidad_organica.nombre + ' - ' + T('Carreras')
    # response.subtitle = T('Carreras')
    return c
