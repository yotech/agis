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
from agiscore.gui.mic import Accion, grid_simple

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Configuración de aulas'),
                           URL('index', args=[request.args(0)]),
                           True),
                    ['index'])

@auth.requires_login()
def index():
    """Configuración de las aulas"""
    C = Storage()
    C.examen = db.examen(int(request.args(0)))
    C.asignatura = C.examen.asignatura_id
    C.evento = db.evento(C.examen.evento_id)
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(T('Años académicos'),
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('evento','index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(db.examen._format(C.examen))
    
    # -- permisos
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # -- configurar grid
    tbl = db.examen_aula
    query = (tbl.id > 0) & (tbl.examen_id == C.examen.id)
    
    if 'new' in request.args:
        tbl.examen_id.default = C.examen.id
        tbl.examen_id.writable = False
        
        estan_set = (db.aula.id > 0) & (db.aula.id == db.examen_aula.aula_id)
        estan = [a.id for a in db(estan_set).select(db.aula.id)]
        a_set  = (db.aula.id > 0) & (db.aula.disponible == True)
        a_set &= (~db.aula.id.belongs(estan))
        posibles = IS_IN_DB(db(a_set), db.aula.id, '%(nombre)s', zero=None)
        db.examen_aula.aula_id.requires = posibles
    
    C.titulo = "{}: {}".format(T("Aulas para el exámen"),
                               db.examen._format(C.examen))
    # -- configurar los campos
    tbl.id.readable = False
    tbl.examen_id.readable = False
    
    C.grid = grid_simple(query,
                         deletable=puede_borrar,
                         searchable=False,
                         args=request.args[:1])
    
    return dict(C=C)