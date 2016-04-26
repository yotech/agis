
# -*- coding: utf-8 -*-
from gluon.storage import Storage
from agiscore.gui.mic import Accion, grid_simple

# TODO: remove
# response.menu = []

menu_lateral.append(Accion(T('Tipos de pagos'),
                           URL('index'),
                           True),
                    ['index'])
menu_lateral.append(Accion(T('Control de pagos'),
                           URL('pagos'),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['pagos'])

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def index():
    C = Storage()
    C.escuela = db.escuela(1)
    menu_migas.append(T("Tipos de pagos"))

    C.titulo = T("Registro de tipos de pago")

    # permisos
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
#     puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))

    tbl = db.tipo_pago

    query = (tbl.id > 0)
    tbl.id.readable = False

    if 'edit' in request.args:
        tbl.nombre.writable = False

    text_lengths = {'tipo_pago.nombre': 50}

    C.grid = grid_simple(query,
                         maxtextlengths=text_lengths,
                         create=puede_crear,
                         editable=puede_editar)

    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def pagos():
    C = Storage()
    C.escuela = db.escuela(1)
    menu_migas.append(T("Control de pagos"))

    C.titulo = T("Registros general de pagos")

    # permisos
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
#     puede_crear = auth.has_membership(role=myconf.take('roles.admin'))

    tbl = db.pago
    query = (tbl.id > 0) & (db.persona.id == tbl.persona_id)

    campos = [tbl.id,
              db.persona.nombre_completo,
              tbl.cantidad,
              tbl.evento_id,]
    tbl.id.readable = True
    for f in db.persona:
        f.readable = False
    db.persona.nombre_completo.readable = True
    db.persona.nombre_completo.label = T("Nombre")
    tbl.persona_id.readable = False
    if 'edit' in request.args:
        tbl.persona_id.readable = True
        tbl.persona_id.writable = False

    text_lengths = {'persona.nombre_completo': 30}

    C.grid = grid_simple(query,
                         field_id=tbl.id,
                         fields=campos,
                         orderby=[db.persona.nombre_completo],
                         create=False,
                         sortable=True,
                         maxtextlength=text_lengths,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         details=True,
                         args=request.args[:1])

    return dict(C=C)
