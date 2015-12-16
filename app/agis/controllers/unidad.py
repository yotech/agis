# -*- coding: utf-8 -*-

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
    from agiscore.gui.mic import MenuLateral, MenuMigas
    menu_lateral = MenuLateral(list())
    menu_migas = MenuMigas()

from gluon.storage import Storage
from agiscore.gui.carrera_uo import grid_carreras_uo
from agiscore.gui.mic import Accion

menu_lateral.append(Accion(T('Carreras'),
                           URL('carreras', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['carreras'])

#TODO: remove
response.menu = []

@auth.requires_login()
def index():
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)
    menu_migas.append(C.unidad.abreviatura or C.unidad.nombre)
    
    # No hace nada aquí, ir agregando las funcionalidades
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def carreras():
    '''configuración de las carreras de la unidad organica'''
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('index', args=[C.unidad.id]),
                    True) # siempre dentro de esta funcion
    menu_migas.append(u_link)
    menu_migas.append(T('Carreras'))
    
    C.grid = grid_carreras_uo(C.unidad, db, T)
    
    return dict(C=C)