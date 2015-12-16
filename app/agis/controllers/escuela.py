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
from agiscore.gui.unidad_organica import manejo_unidades
from agiscore.gui.carrera_ies import grid_carreras_ies
from agiscore.gui.mic import Accion

#TODO: remove
response.menu = []

menu_lateral.append(
    Accion(T('Configurar Escuela'), URL('editar'),
           auth.requires(auth.has_membership(role=myconf.take('roles.admin')))),
    ['editar'])
menu_lateral.append(
    Accion(T('Unidades'), URL('index'),
           (auth.user is not None)),
    ['index'])
menu_lateral.append(
    Accion(T('Infraestructura'), URL('manejo_infraestructura'),
           auth.user),
    ['manejo_infraestructura'])
menu_lateral.append(
    Accion(T('Carreras'), URL('carreras'), True),
    ['carreras'])

@auth.requires_login()
def index():
    C = Storage()
    C.escuela = db.escuela(1)
    # Preparar grid para las unidades
    C.unidades = manejo_unidades(C.escuela, db, T)
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def editar():
    C = Storage()
    C.escuela = db.escuela(1)
    db.escuela.id.readable = False
    C.form = SQLFORM(db.escuela,
                     record=C.escuela,
                     upload=URL('default', 'download'),
                     submit_button=T("Guardar"))
    C.form.add_button(T("Cancelar"), URL('index'))
    if C.form.process().accepted:
        redirect(URL('index'))
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def carreras():
    C = Storage()
    C.escuela = db.escuela(1)
    
    # escoger carreras a utilizar en la escuela
    C.grid = grid_carreras_ies(C.escuela, db, T)
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def manejo_infraestructura():
    db.campus.id.readable = False
    db.edificio.id.readable = False
    db.aula.id.readable = False
    # smargrid se encarga de inicializar estos a los valores corectos
    db.edificio.campus_id.writable = False
    db.aula.edificio_id.writable = False
    manejo = SQLFORM.smartgrid(db.campus,
                               linked_tables=['edificio',
                                              'aula'],
                               csv=False,
                               details=False,
                               # TODO: ver si se puede activar en alguna actulización
                               #       de web2py
                               sortable=False,
                               formname="manejo_infraestructura",
                               showbuttontext=False)
    return dict(manejo=manejo)