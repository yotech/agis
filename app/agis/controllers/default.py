# -*- coding: utf-8 -*-
from applications.agis.modules.base.escuela import Escuela
from applications.agis.modules.db import *

def index():
    """
    Punto de entrada de AGIS.
    """
    # inicializar la aplicación y crear/importar los datos iniciales
    escuela = Escuela()
    # enviar al usuario a su pagina de incio
    redirect(URL('puntoEntrada'))
    return dict()


@auth.requires_login()
def puntoEntrada():
    """
    Direcciona al usuario segun su rol a la vista de inicio que le 
    corresponde
    """
    # inicializar la escuela
    escuela = Escuela()
    # hay que ser explicitos a la hora de cargar las tablas necesarias
    TblEscuela()
    return dict(rows=db(db.escuela.id>0).select())


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


#~ def call():
    #~ """
    #~ exposes services. for example:
    #~ http://..../[app]/default/call/jsonrpc
    #~ decorate with @services.jsonrpc the functions to expose
    #~ supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    #~ """
    #~ return service()


#~ @auth.requires_login()
#~ def api():
    #~ """
    #~ this is example of API with access control
    #~ WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    #~ """
    #~ from gluon.contrib.hypermedia import Collection
    #~ rules = {
        #~ '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        #~ }
    #~ return Collection(db).process(request,response,rules)
