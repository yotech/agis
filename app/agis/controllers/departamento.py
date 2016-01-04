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
from agiscore.gui.mic import Accion
from agiscore.gui.persona import form_crear_persona_ex
from agiscore.gui.mic import grid_simple

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Funsionarios'),
                           URL('index', args=[request.args(0)]),
                           auth.user is not None),
                    ['index'])
menu_lateral.append(Accion(T('Profesores'),
                           URL('claustro', args=[request.args(0)]),
                           auth.user is not None),
                    ['claustro'])

@auth.requires_login()
def claustro():
    '''Gestión del claustro de un departamento'''
    C = Storage()
    C.dpto = db.departamento(int(request.args(0)))
    C.unidad = db.unidad_organica(C.dpto.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    # enlace a la UO
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    # enlace a la opcion carreras de la UO
    c_link = Accion(T('Departamentos'),
                    URL('unidad', 'departamentos', args=[C.unidad.id]),
                    True)
    menu_migas.append(c_link)
    menu_migas.append(C.dpto.nombre)
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    tbl = db.profesor
    query = (tbl.id > 0) & (tbl.persona_id == db.persona.id)
    query &= (tbl.departamento_id == C.dpto.id)
    
    # configurar campos
    db.profesor.persona_id.readable = False
    db.persona.nombre_completo.label = T("Nombre")
    text_length = {'persona.nombre_completo': 100}
    campos = [tbl.id, db.persona.nombre_completo,
              tbl.vinculo,
              tbl.categoria,
              tbl.grado]
    db.profesor.departamento_id.default = C.dpto.id
    db.profesor.departamento_id.writable = False
    
    if 'new' in request.args:
        # recoger los datos personales
        back = URL('claustro', args=[C.dpto.id])
        if session.dcpersona is None:
            (C.grid, data) = form_crear_persona_ex(cancel_url=back,
                                                   db=db,
                                                   T=T,
                                                   session=session,
                                                   request=request)
            if data is None:
                return dict(C=C)
            session.dcpersona = data
        # regoger datos del docente
        form = SQLFORM.factory(db.profesor, submit_button=T('Guardar'))
        title = DIV(H3(T("Datos del docente"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process(dbio=False).accepted:
            persona_id = db.persona.insert(**db.persona._filter_fields(session.dcpersona))
            form.vars.persona_id = persona_id
            db.profesor.insert(**db.profesor._filter_fields(form.vars))
            session.flash = T("Datos del profesor guardados")
            # session cleanup (iss138)
            session.dcpersona = None
            redirect(back)
        C.grid = c        
    else:
        C.grid = grid_simple(query,
                             searchable=True,
                             maxtextlengths=text_length,
                             fields=campos,
                             deletable=puede_borrar,
                             editable=puede_editar,
                             create=puede_crear,
                             args=request.args[:1])
    
    return dict(C=C)

@auth.requires_login()
def index():
    '''Gestión de funsionarios'''
    C = Storage()
    C.dpto = db.departamento(int(request.args(0)))
    C.unidad = db.unidad_organica(C.dpto.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    # enlace a la UO
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    # enlace a la opcion carreras de la UO
    c_link = Accion(T('Departamentos'),
                    URL('unidad', 'departamentos', args=[C.unidad.id]),
                    True)
    menu_migas.append(c_link)
    menu_migas.append(C.dpto.nombre)
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    tbl = db.funsionario
    query  = (tbl.id > 0) & (tbl.persona_id == db.persona.id)
    query &= (tbl.departamento_id == C.dpto.id)
    
    # configurar campos
    tbl.persona_id.readable = False
    db.persona.nombre_completo.label = T("Nombre")
    text_length = {'persona.nombre_completo': 100}
    campos = [tbl.id, db.persona.nombre_completo,
              tbl.vinculo,
              tbl.grado]
    tbl.departamento_id.default = C.dpto.id
    tbl.departamento_id.writable = False
    
    if 'new' in request.args:
        # recoger los datos personales
        back = URL('index', args=[C.dpto.id])
        if session.fcpersona is None:
            (C.grid, data) = form_crear_persona_ex(cancel_url=back,
                                                   db=db,
                                                   T=T,
                                                   session=session,
                                                   request=request)
            if data is None:
                return dict(C=C)
            session.fcpersona = data
        # regoger datos del docente
        form = SQLFORM.factory(db.funsionario, submit_button=T('Guardar'))
        title = DIV(H3(T("Datos del docente"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process(dbio=False).accepted:
            persona_id = db.persona.insert(**db.persona._filter_fields(session.fcpersona))
            form.vars.persona_id = persona_id
            tbl.insert(**tbl._filter_fields(form.vars))
            session.flash = T("Datos del funsionario guardados")
            # session cleanup (iss138)
            session.fcpersona = None
            redirect(back)
        C.grid = c
    else:
        C.grid = grid_simple(query,
                             searchable=True,
                             maxtextlengths=text_length,
                             fields=campos,
                             deletable=puede_borrar,
                             editable=puede_editar,
                             create=puede_crear,
                             args=request.args[:1])
    
    return dict(C=C)
