# -*- coding: utf-8 -*-
from gluon import *
from agiscore.gui.mic import Accion
from agiscore.gui import evento

def enormal_menu(evento_id):
    auth = current.auth
    myconf = current.conf
    T = current.T
    request = current.request
    db = current.db
    menu = []
    sub_menu = []

    ev = db.evento(evento_id)

    item = ('',
        False,
        Accion(ev.nombre, evento.get_url(ev), auth.user != None),
        sub_menu,
        auth.user != None
        )
    sub_menu.append(
        LI(T("Evento"), _class="dropdown-header")
    )
    sub_menu.append((
        '',
        False,
        Accion(T('Configurar evento'),
               URL('enormal', 'configurar', args=[ev.id]),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T("Iniciar candidatura"),
    #            URL('inscripcion', 'inscribir', args=[ev.id]),
    #            (auth.has_membership(role=myconf.take('roles.admin')) or
    #             auth.has_membership(role=myconf.take('roles.incribidor')))),
    #     [],
    #     (auth.has_membership(role=myconf.take('roles.admin')) or
    #      auth.has_membership(role=myconf.take('roles.incribidor')))
    # ))
    sub_menu.append(
        LI('', _role="separator", _class="divider")
    )
    sub_menu.append(
        LI(T("Reportes"), _class="dropdown-header")
    )
    sub_menu.append((
        '',
        False,
        Accion(T('Registro de estudiantes'),
                URL('enormal','matriculados', args=[ev.id]),
                auth.user != None),
        [],
        auth.user != None
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Matriculados por Turma'),
                URL('enormal','matriculados_turma', args=[ev.id]),
                auth.user != None),
        [],
        auth.user != None
    ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('Plazas'),
    #            URL('inscripcion', 'plazas', args=[ev.id]),
    #            auth.user != None),
    #     [],
    #     auth.user != None
    # ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('Asignación Docentes'),
    #            URL('inscripcion','asignaciones', args=[ev.id]),
    #            auth.user != None),
    #     [],
    #     auth.user != None
    # ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('Examenes de acceso'),
    #         URL('inscripcion','examenes', args=[ev.id]),
    #         auth.has_membership(role=myconf.take('roles.admin')) or
    #         auth.has_membership(role=myconf.take('roles.profesor'))),
    #     [],
    #     auth.has_membership(role=myconf.take('roles.admin')) or
    #     auth.has_membership(role=myconf.take('roles.profesor'))
    # ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T("Asignar carreras"),
    #            URL('inscripcion', 'asignar_carreras', args=[ev.id]),
    #            auth.has_membership(role=myconf.take('roles.admin'))),
    #     [],
    #     auth.has_membership(role=myconf.take('roles.admin'))
    # ))
    #
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('Resultados por carrera'),
    #         URL('inscripcion', 'resultados_carrera', args=[ev.id]),
    #         auth.user != None),
    #     [],
    #     auth.user != None
    # ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('Candidaturas por carrera'),
    #         URL('inscripcion', 'candidatos_carreras', args=[ev.id]),
    #         auth.user != None),
    #     [],
    #     auth.user != None
    # ))
    # sub_menu.append((
    #     '',
    #     False,
    #     Accion(T('SEIES 2000'),
    #         URL('inscripcion', 'modelo_2000', args=[ev.id]),
    #         auth.user != None),
    #     [],
    #     auth.user != None
    # ))

    menu += [item]
    return menu
