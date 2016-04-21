# -*- coding: utf-8 -*-
from datetime import datetime
from gluon.storage import Storage
from agiscore.gui.mic import grid_simple
from agiscore.gui.mic import Accion

@auth.requires_login()
def index():
    """Muestra el listado de los años académicos"""
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    menu_migas.append(T('Años académicos'))

    # -- configuración del grid
    tbl = db.ano_academico
    tbl.id.readable = False
    tbl.unidad_organica_id.readable = False
    tbl.descripcion.readable = False
    tbl.nombre.label = T("Año")

    query = (tbl.id > 0) & (tbl.unidad_organica_id == C.unidad.id)

    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))

    crear_link = URL('index', args=[C.unidad.id, 'new'])
    C.crear_link = Accion(CAT(SPAN('', _class='glyphicon glyphicon-plus'),
                                 ' ',
                                 T("Agregar año")),
                             crear_link,
                             puede_crear,
                             _class="btn btn-default btn-xs",
                             _title=T("Agregar un nuevo año académico"))

    if 'new' in request.args:
        # autocrear los años
        ultimo = db(query).select(orderby=[~tbl.nombre]).first()
        if ultimo:
            ultimo = int(ultimo.nombre) + 1
        else:
            # si no existen entonces crear para el actual
            ultimo = datetime.now().year
        key = tbl.insert(nombre=str(ultimo), unidad_organica_id=C.unidad.id,
                         descripcion='')
        from agiscore.db import evento
        evento.crear_eventos(db, key)
        redirect(URL('index', args=[C.unidad.id]))

    def _enlaces(row):
        co = CAT()

        # para cada evento del año agregar un enlace
        q_ev = (db.evento.id > 0)
        q_ev &= (db.evento.ano_academico_id == row.id)

#         from agiscore.gui.evento import controllers_register
        for ev in db(q_ev).select():
#             c = controllers_register[ev.tipo]
            link = URL('evento', 'index', args=[ev.id])
            co.append(LI(A(ev.nombre, _href=link)))
        return co

    C.actual = str(datetime.now().year)

    C.anos = db(query).select(tbl.ALL, orderby=[~tbl.nombre])
    C.enlaces = _enlaces

    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def turmas():
    C = Storage()
    C.unidad = db.unidad_organica(int(request.args(0)))
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    menu_migas.append(T('Turmas'))

    C.titulo = T("Gestión de Turmas")

    tbl = db.turma
    tbl.id.readable = False
    tbl.unidad_organica_id.readable = False
    tbl.unidad_organica_id.writable = False
    tbl.unidad_organica_id.default = C.unidad.id

    query = (tbl.id > 0) & (tbl.unidad_organica_id == C.unidad.id)

    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    text_length = {'turma.carrera_id': 100}

    C.grid = grid_simple(query,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         create=puede_crear,
                         maxtextlength=text_length,
                         args=request.args[:1])

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

    tbl.id.readable = False
    tbl.unidad_organica_id.writable = False
    if 'new' in request.args:
        tbl.unidad_organica_id.default = C.unidad.id

    query = (tbl.id > 0) & (tbl.unidad_organica_id == C.unidad.id)

    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar, puede_borrar = (puede_crear, puede_crear)

    # callbacks
    def onvalidation(form):
        row = None

        if 'new' in request.args:
            dpto_nombre = tbl.nombre.validate(form.vars.nombre)[0]
            row = tbl(nombre=dpto_nombre, unidad_organica_id=C.unidad.id)
        if 'edit' in request.args:
            dpto_nombre = tbl.nombre.validate(form.vars.nombre)[0]
            dpto_id = int(request.args(3))  # args del grid
            q = ((tbl.id != dpto_id) & (tbl.nombre == dpto_nombre))
            row = db(q).select().first()

        if row:
            form.errors.nombre = T("Ya existe en la Unidad Orgánica")

    if 'view' in request.args:
        redirect(URL('departamento', 'index', args=[request.args(3)]))

    C.grid = grid_simple(query,
                         create=puede_crear,
                         deletable=puede_borrar,
                         editable=puede_editar,
                         fields=[tbl.nombre],
                         orderby=[tbl.nombre],
                         onvalidation=onvalidation,
                         searchable=False,
                         details=(auth is not None),
                         args=request.args[:1])

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

    if 'view' in request.args:
        planes_link = URL('carrera',
                          'planes',
                          args=[request.args(3)])
        redirect(planes_link)

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

    C.grid = grid_simple(query,
                       fields=campos,
                       searchable=False,
                       editable=puede_editar,
                       create=puede_crear,
                       deletable=puede_borrar,
                       details=True,
                       maxtextlengths=text_length,
                       args=request.args[:1])

    return dict(C=C)
