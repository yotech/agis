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
from agiscore.db.evento import evento_tipo_represent
from agiscore.validators import IS_DATE_GT

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Configurar evento'),
                           URL('configurar', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['configurar'])

def index():
    """UI evento de inscripción"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    return dict(C=C)

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
    menu_migas.append(C.ano.nombre)
    menu_migas.append(evento_tipo_represent(C.evento.tipo, None))
    
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