# -*- coding: utf-8 -*-
from gluon import current, IS_IN_SET
from agiscore.gui.mic import grid_simple
from agiscore.db.carrera_escuela import carreras_posibles

def grid_carreras_ies(escuela,
                      db,
                      T,
                      auth=None,
                      conf=None,
                      request=None):
    if auth is None:
        auth = current.auth
    if conf is None:
        conf = current.conf
    if request is None:
        request = current.request
        
    model = db.carrera_escuela
        
    editar = (auth.has_membership(role=conf.take('roles.admin')))
    crear = (auth.has_membership(role=conf.take('roles.admin')))
    deletable = (auth.has_membership(role=conf.take('roles.admin')))
    
    query = (model.id > 0)
    model.id.readable = False
    orden = [model.descripcion_id]
    campos = [model.id,
              model.codigo,
              model.descripcion_id]
    text_length = {"carrera_escuela.descripcion_id": 100}
    
    if 'new' in request.args:
        posibles = carreras_posibles(db)
        model.descripcion_id.requires = IS_IN_SET(posibles, zero=None)
    if 'edit' in request.args:
        model.descripcion_id.writable = False
    
    grid = grid_simple(query,
                       fields=campos,
                       orderby=orden,
                       maxtextlengths=text_length,
                       create=crear,
                       editable=editar,
                       deletable=deletable)
    
    return grid
