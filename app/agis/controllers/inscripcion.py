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
from agiscore.db.evento import evento_tipo_represent
from agiscore.validators import IS_DATE_GT
from datetime import date

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Configurar evento'),
                           URL('configurar', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['configurar'])
menu_lateral.append(Accion(T('Registro de candidatos'),
                           URL('candidaturas', args=[request.args(0)]),
                           True),
                    ['candidaturas'])

@auth.requires_login()
def index():
    """UI evento de inscripción"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    return dict(C=C)

# TODO: chequear más tade si se pueden poner restricciones adicionales
@auth.requires_login()
def candidaturas():
    '''Mostrar el registro de candidatos para el evento de inscripción'''
    C = Storage()
    C.evento = db.evento(request.args(0))
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
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Candidaturas"))
    
    # --permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin')) 
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    from agiscore.db.evento import esta_activo
    # puede_crear aqui es si el usuario puede inscribir candidatos
    puede_crear &= esta_activo(C.evento)
    
    C.crear = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                         ' ',
                         T("Iniciar candidatura")),
                     URL('inscribir', args=[C.evento.id]),
                     puede_crear,
                     _class="btn btn-default")
    
    # -- preparar el grid
    tbl = db.candidatura
    
    # -- configurar consulta
    query  = (tbl.id > 0)
    query &= (tbl.ano_academico_id == C.ano.id)
    query &= (tbl.estudiante_id == db.estudiante.id)
    query &= (db.estudiante.persona_id == db.persona.id)
    
    C.grid = grid_simple(query,
                         create=False,
                         editable=False,
                         deletable=puede_borrar,
                         args=request.args[:1])
    
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def configurar():
    """Configuración del evento"""
    C = Storage()
    C.evento = db.evento(request.args(0))
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
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Ajustes"))
    
    # configurar campos
    tbl = db.evento
    tbl.id.readable = False
    tbl.nombre.writable = False
    tbl.nombre.readable = False
    tbl.tipo.readable = False
    tbl.tipo.writable = False
    tbl.ano_academico_id.writable = False
    tbl.ano_academico_id.readable = False
    
    if request.vars.fecha_inicio:
        # validar que la fecha de inicio este antes que la de fin
        (fecha_inicio, msg) = db.evento.fecha_inicio.validate(
            request.vars.fecha_inicio)
        if msg is None:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(),
                                            IS_DATE_GT(minimum=fecha_inicio)]
        else:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(), IS_DATE()]
    
    C.form = SQLFORM(db.evento, record=C.evento, submit_button=T("Guardar"))
    C.form.add_button(T("Cancelar"), URL('index', args=[C.evento.id]))
    
    if C.form.process().accepted:
        session.flash = T("Ajustes guardados")
        redirect(URL('index', args=[C.evento.id]))

    return dict(C=C)