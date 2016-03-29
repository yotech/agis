# -*- coding: utf-8 -*-

from gluon import *
from agiscore.gui.mic import Accion

def escuela_menu():
    """
    Retorna la estructura del menú para la escuela
    """
    request = current.request
    auth = current.auth
    myconf = current.conf
    T = current.T
    menu = []
    sub_menu = []

    esc_item = ('',
        (True if request.controller == 'escuela' else False),
        Accion('Escuela', URL('escuela', 'index'), auth.user != None),
        sub_menu,
        auth.user != None
        )
    sub_menu.append((
        '',
        False,
        Accion(T('Configurar IES'), URL('escuela', 'editar'),
            auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Carreras del IES'), URL('escuela', 'carreras'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Carreras (ME)'), URL('escuela','carreras_me'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Unidades Orgánicas'), URL('escuela', 'index'),
               (auth.user is not None)),
        [],
        (auth.user is not None)
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Infraestructura'), URL('escuela','infraestructura'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Centros enseñanza media'), URL('escuela','media'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Asignaturas'), URL('escuela', 'asignaturas'),
               auth.has_membership(role=myconf.take('roles.admin')),
               _title=T("Registro general de asignaturas")),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Registro de Personas'), URL('escuela','personas'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Contabilidad'), URL('gcontable', 'index'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Seguridad'), URL('appadmin', 'manage', args=['auth']),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))

    menu += [esc_item]
    return menu
