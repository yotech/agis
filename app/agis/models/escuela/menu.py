from agiscore.gui.mic import Accion

def _():
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
        Accion(T('Configurar IES'), URL('editar'),
            auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Carreras del IES'), URL('carreras'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Carreras (ME)'), URL('carreras_me'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Unidades Orgánicas'), URL('index'),
               (auth.user is not None)),
        [],
        (auth.user is not None)
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Infraestructura'), URL('infraestructura'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Centros enseñanza media'), URL('media'),
               auth.has_membership(role=myconf.take('roles.admin'))),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Asignaturas'), URL('asignaturas'),
               auth.has_membership(role=myconf.take('roles.admin')),
               _title=T("Registro general de asignaturas")),
        [],
        auth.has_membership(role=myconf.take('roles.admin'))
    ))
    sub_menu.append((
        '',
        False,
        Accion(T('Registro de Personas'), URL('personas'),
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

if not request.ajax:
    response.menu += _()
