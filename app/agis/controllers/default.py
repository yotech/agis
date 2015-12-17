# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

if False:
    from gluon import *
    from db import *
    from menu import *
    from tables import *
    from gluon.contrib.appconfig import AppConfig
    from gluon.tools import Auth, Service, PluginManager
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = DAL('sqlite://storage.sqlite')
    myconf = AppConfig(reload=True)
    auth = Auth(db)
    service = Service()
    plugins = PluginManager()

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # redirect(URL('escuela', 'index'))
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


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


@auth.requires_membership(myconf.take('roles.admin'))
def editar_persona():
    """componente para la edición de los datos de una persona"""
    if not request.vars.persona_id:
        raise HTTP(404)
    from agiscore.gui import persona as p_gui
    p = db.persona(int(request.vars.persona_id))
    c, f = p_gui.form_editar(p.uuid)
    if f.process().accepted:
        response.flash = T('Cambios guardados')
        response.js = "jQuery('#%s').get(0).reload()" % request.cid
    return dict(componente=c)

@auth.requires_membership(myconf.take('roles.admin'))
def editar_usuario():
    """componente para editar un usuario asociado a una persona"""
    # Si la persona no tiene usuario asociado se crea uno nuevo
    # y se asocia a la persona.
    from agiscore.db import persona as persona_model
    if not request.vars.persona_id:
        raise HTTP(404)
    p = db.persona(int(request.vars.persona_id))
    if not p.user_id:
        # crear un usuario para la persona con una contraseña cualquiera
        if not p.email:
            # sin correo no hay usuario
            title = H3(T("Debe establecer un correo electrónico"))
            body = P(T("""
                La persona no tiene asocido un correo electrónico, lo cual es
                necesario para acceder al sistema.
                """))
            c = CAT(title, DIV(body,
                               _class="alert alert-danger",
                               role="alert"))
            return dict(componente=c)
        else:
            # crear el usuario
            persona_model.crear_usuario(p)

    title = H3(T("Información"))
    body = P(T("""
        La persona tiene asociado un usuario valido.
        """))
    c = CAT(title, DIV(body, _class="alert alert-success", role="alert"))
    return dict(componente=c)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


# def call():
#     """
#     exposes services. for example:
#     http://..../[app]/default/call/jsonrpc
#     decorate with @services.jsonrpc the functions to expose
#     supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
#     """
#     return service()


# @auth.requires_login()
# def api():
#     """
#     this is example of API with access control
#     WEB2PY provides Hypermedia API (Collection+JSON) Experimental
#     """
#     from gluon.contrib.hypermedia import Collection
#     rules = {
#         '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
#         }
#     return Collection(db).process(request,response,rules)
