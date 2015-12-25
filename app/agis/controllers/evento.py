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

from agiscore.db.evento import INSCRIPCION, MATRICULA

@auth.requires_login()
def index():
    ev = db.evento(int(request.args(0)))
    if ev.tipo == INSCRIPCION:
        redirect(URL('inscripcion', 'index', args=[ev.id]))
    if ev.tipo == MATRICULA:
        redirect(URL('matricula', 'index', args=[ev.id]))
    return dict()