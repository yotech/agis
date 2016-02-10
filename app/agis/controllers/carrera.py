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
from agiscore.db.carrera_uo import carrera_uo_format

# TODO: remove
response.menu = []


menu_lateral.append(
    Accion(T('Planes'), URL('planes', args=[request.args(0)]),
           auth.has_membership(role=myconf.take('roles.admin'))),
    ['planes', 'asignaturas'])
menu_lateral.append(
    Accion(T('Especialidades'), URL('especialidades', args=[request.args(0)]),
           auth.has_membership(role=myconf.take('roles.admin'))),
    ['especialidades'])


@auth.requires_login()
def index():
    C = Storage()
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def especialidades():
    C = Storage()
    C.carrera = db.carrera_uo(int(request.args(0)))
    C.unidad = db.unidad_organica(C.carrera.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    C.carrera_format = carrera_uo_format(C.carrera)
    # breadcumbs
    # enlace a la UO
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    # enlace a la opcion carreras de la UO
    c_link = Accion(T('Carreras'),
                    URL('unidad', 'carreras', args=[C.unidad.id]),
                    True)
    menu_migas.append(c_link)
    # planes
    C.carrera_format = carrera_uo_format(C.carrera)
    menu_migas.append(C.carrera_format)
    menu_migas.append(T("Especialidades"))
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    tbl = db.especialidad
    tbl.carrera_id.default = C.carrera.id
    tbl.carrera_id.readable = False
    tbl.carrera_id.writable = False
    tbl.id.readable = False
    
    if ('new' in request.args) or ('edit' in request.args):
        dbset = (tbl.carrera_id == C.carrera.id)
        tbl.nombre.requires.append(IS_NOT_IN_DB(db(dbset),
                                                'especialidad.nombre'))
        tbl.abreviatura.requires.append(IS_NOT_IN_DB(db,
                                                     'especialidad.abreviatura'))
    
    query = (tbl.id > 0) & (tbl.carrera_id == C.carrera.id)
    C.grid = grid_simple(query,
                         create=puede_crear,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         args=request.args[:1])
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def asignaturas():
    C = Storage()
    C.plan = db.plan_curricular(int(request.args(0)))
    C.carrera = db.carrera_uo(C.plan.carrera_id)
    C.unidad = db.unidad_organica(C.carrera.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    # enlace a la UO
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    # enlace a la opcion carreras de la UO
    c_link = Accion(T('Carreras'),
                    URL('unidad', 'carreras', args=[C.unidad.id]),
                    True)
    menu_migas.append(c_link)
    # planes
    C.carrera_format = carrera_uo_format(C.carrera)
    menu_migas.append(C.carrera_format)
    p_link = Accion(T('Planes'),
                    URL('planes', args=[C.carrera.id]),
                    True)
    menu_migas.append(p_link)
    menu_migas.append(C.plan.nombre)
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # -- contruir el grid
    tbl = db.asignatura_plan
    tbl.id.readable = False
    query = (tbl.id > 0)
    query &= (tbl.plan_curricular_id == C.plan.id)
    
    tbl.plan_curricular_id.readable = False
    if ('new' in request.args) or ('edit' in request.args):
        tbl.plan_curricular_id.writable = False
        tbl.plan_curricular_id.default = C.plan.id
        
    if 'edit' in request.args:
        tbl.asignatura_id.writable = False
        tbl.nivel_academico_id.writable = False
        tbl.importancia.default = 100
    
    # validar que no se  repitan las asignaturas por nivel
    def onvalidation(form):
        if 'new' in request.args:
            # comprobar que no exista la combinación nivel
            n_id = tbl.nivel_academico_id.validate(form.vars.nivel_academico_id)[0]
            a_id = tbl.asignatura_id.validate(form.vars.asignatura_id)[0]
            row = tbl(nivel_academico_id=n_id,
                      asignatura_id=a_id,
                      plan_curricular_id=C.plan.id)
            if row:
                # ya existe en el plan esa asignatura con el mismo nivel de
                # acceso
                form.errors.asignatura_id = T("Ya existe en el plan con el mismo nivel")
    
    text_lengths = {'asignatura_plan.asignatura_id': 50}
    
    C.grid = grid_simple(query,
                         args=request.args[:1],
                         editable=puede_crear,
                         deletable=puede_borrar,
                         create=puede_crear,
                         onvalidation=onvalidation,
                         maxtextlengths=text_lengths,
                         orderby=[tbl.nivel_academico_id, tbl.asignatura_id],)
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def planes():
    '''Manejo de planes para una carrera'''
    C = Storage()
    C.carrera = db.carrera_uo(int(request.args(0)))
    C.unidad = db.unidad_organica(C.carrera.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    # enlace a la UO
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    # enlace a la opcion carreras de la UO
    c_link = Accion(T('Carreras'),
                    URL('unidad', 'carreras', args=[C.unidad.id]),
                    True)
    menu_migas.append(c_link)
    # planes
    C.carrera_format = carrera_uo_format(C.carrera)
    menu_migas.append(C.carrera_format)
    menu_migas.append(T("Planes"))
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    # -- contruir el grid de los planes
    tbl = db.plan_curricular
    query = ((tbl.id > 0) & (tbl.carrera_id == C.carrera.id))
    
    # ver si es la opción de activar plan
    if 'activar' in request.args:
        plan = tbl(int(request.args(2)))
        # desactivar todos los planes
        db(query).update(estado=False)
        plan.update_record(estado=True)
        redirect(URL('carrera', 'planes', args=[C.carrera.id]))
    
    tbl.id.readable = False
    tbl.carrera_id.writable = False
    
    if 'new' in request.args:
        tbl.carrera_id.default = C.carrera.id    
    
    campos = [tbl.nombre, tbl.estado]
    
    def _enlaces(row):
        co = CAT()
        link = URL('asignaturas', args=[row.id])
        txt = CAT(SPAN('', _class="glyphicon glyphicon-book"),
                  ' ',
                  T('Asignaturas'))
        co.append(Accion(txt, link, True, _class="btn btn-default btn-sm"))
        if not row.estado:
            link = URL('planes',
                       args=[C.carrera.id, 'activar', row.id],
                       user_signature=True)
            txt = CAT(SPAN('', _class="glyphicon glyphicon-ok-sign"),
                      ' ',
                      T("Activar"))
            co.append(Accion(txt, link, True,
                             _class="btn btn-default btn-sm"))
        return co
    
    enlaces = [dict(header='', body=_enlaces)]
    
    C.grid = grid_simple(query,
                         create=puede_crear,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         fields=campos,
                         links=enlaces,
                         args=request.args[:1])
    
    return dict(C=C)
