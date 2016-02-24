# -*- coding: utf-8 -*-

from gluon import current
from gluon import IS_IN_DB
from agiscore.gui.mic import grid_simple
from agiscore.db import provincia
from agiscore.db import municipio
from agiscore.db import tipos_ensennanza as tipo_escuela

def manejo_escuelas_medias(db, T, auth=None, request=None, conf=None):
    if auth is None:
        auth = current.auth
    if request is None:
        request = current.request
    if conf is None:
        conf = current.conf

    if 'new' in request.args:
        #preparar el formulario para agregar un elemento.
        if request.vars.provincia_id:
            prov = provincia.obtener(int(request.vars.provincia_id))
        else:
            prov = provincia.obtener() # obtener cualquier provincia
        mun = municipio.obtener(provincia_id=prov.id)
        db.escuela_media.provincia_id.default = prov.id
        db.escuela_media.municipio_id.default = mun.id
        db.escuela_media.municipio_id.requires = IS_IN_DB(
            db(db.municipio.provincia_id == prov.id),
            'municipio.id',"%(nombre)s",zero=None
        )
        db.escuela_media.codigo.comment = T("Código de 4 digitos")
    condq = (db.escuela_media.tipo_escuela_media_id !=
             tipo_escuela.obtener_por_uuid(tipo_escuela.ID_PROTEGIDO).id)
    db.escuela_media.provincia_id.show_if = condq
    db.escuela_media.municipio_id.show_if = condq
    db.escuela_media.id.readable = False
    # esto debe mantenerse lo más proximo posible a la contrucción del GRID
    if ('new' in request.args) or ('edit' in request.args):
        if request.vars.tipo_escuela_media_id:
            # guardando el formulario
            sid = int(request.vars.tipo_escuela_media_id)
            pid = tipo_escuela.obtener_por_uuid(tipo_escuela.ID_PROTEGIDO).id
            if sid == pid: # si es el valor ID_PROTEGIDO
                # asignarle valores a la provincia y municipo
                id_p = db.provincia.obtener_por_uuid(provincia.ID_PROTEGIDO).id
                id_m = db.municipio.obtener_por_uuid(municipio.ID_PROTEGIDO).id
                request.vars.provincia_id = id_p
                request.vars.municipio_id = id_m
                request.post_vars.provincia_id = id_p
                request.post_vars.municipio_id = id_m
                db.escuela_media.provincia_id.default = id_p
                db.escuela_media.municipio_id.default = id_m
                db.escuela_media.municipio_id.requires = []
    
    puede_crear = auth.has_membership(role=conf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    text_lengths = {'escuela_media.nombre': 100}
    
    manejo = grid_simple((db.escuela_media.id > 0),
                         maxtextlength=text_lengths,
                         create=puede_crear,
                         editable=puede_editar,
                         deletable=puede_borrar)
    
    return manejo