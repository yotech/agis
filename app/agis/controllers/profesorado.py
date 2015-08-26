# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules.db import persona
from applications.agis.modules.db import provincia
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules.db import profesor_asignatura
from applications.agis.modules.db import profesor

sidenav.append(
    [T('Listado general'), # Titulo del elemento
    URL('listado_general'), # url para el enlace
    ['listado_general'],] # en funciones estará activo este item
)

sidenav.append(
    [T('Agregar profesor'), # Titulo del elemento
     URL('agregar_profesor'), # url para el enlace
     ['agregar_profesor'],] # en funciones estará activo este item
)

sidenav.append(
    [T('Asignar asignatura'), # Titulo del elemento
     URL('asignar_asignatura'), # url para el enlace
     ['asignar_asignatura'],] # en funciones estará activo este item
)
migas.append(
    tools.split_drop_down(
        Storage(dict(url='#', texto=T('Recursos Humanos'))),
        [Storage(dict(url=URL('profesorado','index'),
                      texto=T('Profesorado'))),
        ]
        )
    )
migas.append(A(T('Profesorado'), _href=URL('index')))

def index():
    redirect( URL( 'listado_general' ) )
    return dict(message="hello from profesorado.py")

@auth.requires_membership('administrators')
def asignar_asignatura():
    form = SQLFORM( db.profesor_asignatura,formstyle='bootstrap',
        submit_button=T( 'Guardar y agregar nuevo' )
        )
    if form.process().accepted:
        session.flash=T( 'Asignatura asignada' )
        redirect( URL( 'asignar_asignatura' ) )
    return dict( sidenav=sidenav,form=form )

@auth.requires_membership('administrators')
def listado_general():
    migas.append(T('Listado general'))
    manejo=profesor.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def agregar_profesor():
    if not request.args(0):
        redirect( URL( 'agregar_profesor',args=['1'] ) )
    step = request.args(0)
    form = None

    if step == '1':
        # paso 1: datos personales
        db.persona.lugar_nacimiento.widget = SQLFORM.widgets.autocomplete(request,
            db.comuna.nombre,id_field=db.comuna.id )
        if request.vars.email:
            db.persona.email.requires = IS_EMAIL( error_message='La dirección de e-mail no es valida' )
        else:
            db.persona.email.requires = None
        # preconfiguración de las provincias, municipios y comunas
        if request.vars.dir_provincia_id:
            provincia_id = int(request.vars.dir_provincia_id)
        else:
            sede_central = escuela.obtener_sede_central()
            provincia_id = sede_central.provincia_id
        db.persona.dir_provincia_id.default = provincia_id
        municipios = municipio.obtener_posibles( provincia_id )
        if request.vars.dir_municipio_id:
            dir_municipio_id = int(request.vars.dir_municipio_id)
        else:
            dir_municipio_id,nombre = municipios[0]
        db.persona.dir_municipio_id.default = dir_municipio_id
        if request.vars.dir_comuna_id:
            db.persona.dir_comuna_id.default = int(request.vars.dir_comuna_id)
        db.persona.dir_municipio_id.requires = IS_IN_SET( municipios,zero=None )
        comunas = comuna.obtener_posibles( dir_municipio_id )
        db.persona.dir_comuna_id.requires = IS_IN_SET( comunas,zero=None )
        form = SQLFORM.factory( db.persona, submit_button=T( 'Siguiente' ) )
        if form.process(dbio=False).accepted:
            # guardar los datos de persona y pasar el siguiente paso
            p = dict(nombre=form.vars.nombre,
                apellido1=form.vars.apellido1,
                apellido2=form.vars.apellido2,
                fecha_nacimiento=form.vars.fecha_nacimiento,
                genero=form.vars.genero,
                lugar_nacimiento=form.vars.lugar_nacimiento,
                estado_civil=form.vars.estado_civil,
                tipo_documento_identidad_id=form.vars.tipo_documento_identidad_id,
                numero_identidad=form.vars.numero_identidad,
                nombre_padre=form.vars.nombre_padre,
                nombre_madre=form.vars.nombre_madre,
                estado_politico=form.vars.estado_politico,
                nacionalidad=form.vars.nacionalidad,
                dir_provincia_id=form.vars.dir_provincia_id,
                dir_municipio_id=form.vars.dir_municipio_id,
                dir_comuna_id=form.vars.dir_comuna_id,
                direccion=form.vars.direccion,
                telefono=form.vars.telefono,
                email=form.vars.email
            )
            session.persona = p
            redirect( URL( 'agregar_profesor',args=['2'] ) )
    elif step == '2':
        db.profesor.persona_id.readable = False
        form = SQLFORM.factory( db.profesor, submit_button=T( 'Guardar' ) )
        if form.process(dbio=False).accepted:
            persona_id = db.persona.insert( **db.persona._filter_fields( session.persona ) )
            form.vars.persona_id = persona_id
            db.profesor.insert( **db.profesor._filter_fields( form.vars ) )
            session.persona = None
            session.flash = T( "Datos del profesor guardados" )
            redirect( URL( 'agregar_profesor',args=['1'] ) )
    return dict( sidenav=sidenav,form=form,step=step )
