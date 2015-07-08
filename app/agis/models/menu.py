# -*- coding: utf-8 -*-
from applications.agis.modules import menu
# this file is released under public domain and you can use without limitations


#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                  _class="brand",_href="http://www.web2py.com/")
response.logo = A("SIGA", _class="brand", _href="#")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = []
sidenav = []


if session.menu:
    response.menu = session.menu
else:
    menu.agregar_elemento( response.menu,( T('Inicio'),False,URL('default', 'index'), [] ),
        ['administrators'],
    )
    menu.agregar_elemento( response.menu,( T('Configuración'),False,'#',[] ),['administrators'] )
    menu.agregar_elemento( response.menu,( T('Docentes'),False,'#',[] ),['administrators'] )
    menu.agregar_elemento( response.menu,( T('Contabilidad'),False,'#',[] ),['administrators'] )
    menu.agregar_elemento( response.menu,( T('Recursos Humanos'),False,'#',[] ),['administrators'] )
    menu.agregar_elemento(response.menu,
        (T('Candidatos'),False,URL('candidatura','index'),[]),
        ['administrators'],
        T('Docentes')
    )
    menu.agregar_elemento(response.menu,
        (T('Estudiantes'),False,URL('estudiantes','index'),[]),
        ['administrators'],
        T('Docentes')
    )
    menu.agregar_elemento(response.menu,
        (T('General'),False,URL('general','index'),[]),
        ['administrators'],
        T('Configuración')
    )
    menu.agregar_elemento(response.menu,
        (T('Institución'), False, URL('instituto','index'), []),
        ['administrators'],
        T('Configuración')
    )
    menu.agregar_elemento(response.menu,(T('Organización Docente'),False,'#',[]),['administrators'],T('Institución'))
    menu.agregar_elemento(response.menu,(T('Organización Educacional'),False,'#',[]),['administrators'],T('Institución'))
    menu.agregar_elemento(response.menu,
        (T('Infraestructura'),False,URL('infraestructura','index'),[]),
        ['administrators'],
        T('Institución')
    )
    menu.agregar_elemento(response.menu,
        (T('Departamentos'),False,URL('instituto','departamentos'),[]),
        ['administrators'],
        T('Institución')
    )
    menu.agregar_elemento(response.menu,
        (T('Eventos'),False,URL('instituto','eventos'),[]),
        ['administrators'],
        T('Institución')
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Escuela'), False, URL('instituto','configurar_escuela'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Organización Docente') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Unidades Orgánicas'), False, URL('instituto', 'gestion_uo'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Organización Docente') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Selección de Régimen a Realizar en la UO'), False, URL('instituto', 'asignar_regimen'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Organización Docente') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Selección de Carreras a Impartir en la UO'), False, URL('instituto', 'asignar_carrera'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Organización Docente') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Años Académicos'), False, URL('instituto', 'ano_academico'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Organización Docente') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Regiones Académicas'), False, URL('general', 'region_academica'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Carreras'), False, URL('general', 'descripcion_carrera'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Localidades'), False, URL('general', 'localidades'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Régimen'), False, URL('general', 'regimen'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Tipos de Enseñanza Media'), False, URL('general', 'tipos_ensennaza'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Escuelas de Enseñanza Media'), False, URL('general', 'escuela_media'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestión de Tipos de Documentos de Identidad'), False, URL('general', 'tipo_documento_identidad'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Gestionar Necesidades Especiales de Educación'), False, URL('general', 'tipo_discapacidad'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('General') # padre
    )
#     menu.agregar_elemento(response.menu, # a que menu agregar
#         (T('Listado de Candidatos'), False, URL('candidatura', 'index'), []), # item a agregar
#         ['administrators'], # roles que pueden ver esto
#         T('Candidatos') # padre
#     )
    menu.agregar_elemento(response.menu, # a que menu agregar
        (T('Iniciar Candidatura'), False, URL('candidatura', 'iniciar_candidatura'), []), # item a agregar
        ['administrators'], # roles que pueden ver esto
        T('Candidatos') # padre
    )
    menu.agregar_elemento(response.menu,
        (T('Gestionar Campus'),False,URL('infraestructura','gestion_campus'),[]),
        ['administrators'],
        T('Infraestructura')
    )
    menu.agregar_elemento(response.menu,
        (T('Gestionar Edificio'),False,URL('infraestructura','gestion_edificio'),[]),
        ['administrators'],
        T('Infraestructura')
    )
    menu.agregar_elemento(response.menu,
        (T('Gestionar Aula'),False,URL('infraestructura','gestion_aula'),[]),
        ['administrators'],
        T('Infraestructura')
    )
    menu.agregar_elemento(response.menu,
        (T('Configuración General'),False,URL('contabilidad','index'),[]),
        ['administrators'],
        T('Contabilidad')
    )
    menu.agregar_elemento(response.menu,
        (T('Tipos de Pagos'),False,URL('contabilidad','tipo_pago'),[]),
        ['administrators'],
        T('Configuración General')
    )
    menu.agregar_elemento(response.menu,
        (T('Profesorado'),False,URL('profesorado','index'),[]),
        ['administrators'],
        T('Recursos Humanos')
    )
#     menu.agregar_elemento(response.menu,
#         (T('Listado General'),False,URL('profesorado','listado_general'),[]),
#         ['administrators'],
#         T('Profesorado')
#     )
    menu.agregar_elemento(response.menu,
        (T('Asignar asignatura'),False,URL('profesorado','asignar_asignatura'),[]),
        ['administrators'],
        T('Profesorado')
    )
    menu.agregar_elemento(response.menu,
        (T('Agregar Profesor'),False,URL('profesorado','agregar_profesor'),[]),
        ['administrators'],
        T('Profesorado')
    )
    menu.agregar_elemento(response.menu,
        (T('Niveles Académicos'),False,URL('instituto','nivel_academico'),[]),
        ['administrators'],
        T('Organización Educacional')
    )
    menu.agregar_elemento(response.menu,
        (T('Grupos de estudiantes'),False,URL('instituto','grupos'),[]),
        ['administrators'],
        T('Organización Educacional')
    )
    menu.agregar_elemento(response.menu,
        (T('Asignaturas'),False,URL('instituto','asignaturas'),[]),
        ['administrators'],
        T('Organización Educacional')
    )
    menu.agregar_elemento(response.menu,
        (T('Planes Curriculares'),False,URL('instituto','planes_curriculares'),[]),
        ['administrators'],
        T('Organización Educacional')
    )
    menu.agregar_elemento(response.menu,
        (T('Plazas de Estudiantes a Otorgar'),False,URL('instituto','plazas_estudiantes'),[]),
        ['administrators'],
        T('Organización Educacional')
    )
    menu.agregar_elemento(response.menu,
        (T('Registrar pago'),False,"#",[]),
        ['administrators'],
        T('Contabilidad')
    )
    menu.agregar_elemento(response.menu,
        (T('Inscripción'),False,URL('contabilidad','registrar_pago_inscripcion'),[]),
        ['administrators'],
        T('Registrar pago')
    )
    session.menu = response.menu


DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('web2py', _class='highlighted'), False, 'http://web2py.com', [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, URL('admin', 'default', 'design/%s' % app), [
        (T('Controller'), False,
         URL(
         'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
        (T('View'), False,
         URL(
         'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
        (T('Layout'), False,
         URL(
         'admin', 'default', 'edit/%s/views/layout.html' % app)),
        (T('Stylesheet'), False,
         URL(
         'admin', 'default', 'edit/%s/static/css/web2py.css' % app)),
        (T('DB Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/db.py' % app)),
        (T('Menu Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/menu.py' % app)),
        (T('Database'), False, URL(app, 'appadmin', 'index')),
        (T('Errors'), False, URL(
         'admin', 'default', 'errors/' + app)),
        (T('About'), False, URL(
         'admin', 'default', 'about/' + app)),
        ]),
            ('web2py.com', False, 'http://www.web2py.com', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Layouts'), False, 'http://web2py.com/layouts'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             (T('Semantic'), False, 'http://web2py.com/semantic'),
             ]),
            (T('Documentation'), False, 'http://www.web2py.com/book', [
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Buy this book'), False,
              'http://stores.lulu.com/web2py'),
             ]),
            (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
                        (T('Twitter'), False, 'http://twitter.com/web2py'),
                        (T('Live Chat'), False,
                         'http://webchat.freenode.net/?channels=web2py'),
                        ]),
                (T('Plugins'), False, None, [
                        ('plugin_wiki', False,
                         'http://web2py.com/examples/default/download'),
                        (T('Other Plugins'), False,
                         'http://web2py.com/plugins'),
                        (T('Layout Plugins'),
                         False, 'http://web2py.com/layouts'),
                        ])
                ]
         )]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
