# -*- coding: utf-8 -*-
if False:
    from gluon import *
    from db import *
    from menu import *
    from menu import menu_lateral, menu_migas
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

from gluon.storage import Storage
from agiscore.db import campus
from agiscore.db import edificio
from agiscore.db import aula
from agiscore.gui.mic import Accion

rol_admin = auth.has_membership(myconf.take('roles.admin'))

menu_lateral.append(
    Accion(T('Gestionar campus'),
           URL('gestion_campus'), rol_admin),
    ['gestion_campus'])

menu_lateral.append(
    Accion(T('Gestionar edificios'),
           URL('gestion_edificio'), rol_admin),
    ['gestion_edificio'])

menu_lateral.append(
    Accion(T('Gestionar aulas'),
           URL('gestion_aula'), rol_admin),
    ['gestion_aula'])

menu_migas.append(Accion(T('Configuración'), '#', True))
menu_migas.append(
    Accion(T('Infraestructura'), URL('index'), rol_admin))

def index():
    redirect( URL( 'gestion_campus' ) )
    return dict(message="hello from infraestructura.py")

@auth.requires(rol_admin)
def gestion_edificio():
    menu_migas.append(T('Gestión de edificios'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = edificio.obtener_manejo()
    return dict(manejo=manejo )

@auth.requires(rol_admin)
def gestion_aula():
    menu_migas.append(T('Gestión de aulas'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = aula.obtener_manejo()
    return dict( manejo=manejo )

@auth.requires(rol_admin)
def gestion_campus():
    menu_migas.append(T('Gestión de campus'))
    manejo = campus.obtener_manejo()
    return dict( manejo=manejo )
