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
from agiscore.gui.mic import grid_simple
from agiscore.gui.mic import Accion

menu_lateral.append(Accion(T('Departamentos'),
                           URL('departamentos', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['departamentos'])
menu_lateral.append(Accion(T('Carreras'),
                           URL('carreras', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['carreras'])


# TODO: remove
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
def departamentos():
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    menu_migas.append(T('Departamentos'))
    
    # -- configurar grid
    tbl = db.departamento
    
    query = (tbl.id > 0) & (tbl.unidad_organica_id == C.unidad.id)
    
    return dict(C=C)    

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def carreras():
    '''configuración de las carreras de la unidad organica'''
    from agiscore.db import carrera_uo as model
    
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    menu_migas.append(T('Carreras'))
    
    tbl = db.carrera_uo
        
    query = (tbl.id > 0)
    query &= (tbl.unidad_organica_id == C.unidad.id)
    
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    tbl.unidad_organica_id.writable = False
    tbl.carrera_escuela_id.label = T("Carrera")
    
    if 'new' in request.args:
        tbl.unidad_organica_id.default = C.unidad.id
        posibles = model.obtener_posibles(db, C.unidad.id)
        if not posibles:
            # si no hay carreras para seleccionar, volver al incio
            msg = T('No hay más carreras definidas en la escuela')
            session.flash = msg
            redirect(URL('carreras', args=[C.unidad.id]))
        tbl.carrera_escuela_id.requires = IS_IN_SET(posibles, zero=None)
    
    campos = [tbl.carrera_escuela_id]
    text_length = {'carrera_uo.carrera_escuela_id': 60}
    
    def _enlaces(row):
        co = CAT()
        planes_link = URL('carrera', 'planes', args=[row.id])
        co.append(Accion(CAT(SPAN('', _class='glyphicon glyphicon-cog'),
                                 ' ',
                                 T('Planes')),
                             planes_link,
                             True,
                             _class="btn btn-default"))
        return co
    
    enlaces = [dict(header='', body=_enlaces)]
    if 'new' in request.args or 'edit' in request.args:
        # quitar los enlaces en los formularios
        enlaces = []
    
    C.grid = grid_simple(query,
                       fields=campos,
                       searchable=False,
                       editable=puede_editar,
                       create=puede_crear,
                       deletable=puede_borrar,
                       maxtextlengths=text_length,
                       links=enlaces,
                       args=request.args[:1])
    
    return dict(C=C)
