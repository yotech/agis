# -*- coding: utf-8 -*-
from applications.agis.modules.db import escuela
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import persona
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules import tools

sidenav.append(
    [T('Iniciar candidatura'), # Titulo del elemento
     URL('iniciar_candidatura'), # url para el enlace
     ['iniciar_candidatura'],] # en funciones estará activo este item
)

def index(): return dict( message="hello from candidatura.py" )


@auth.requires_membership('administrators')
def obtener_comunas():
    # TODO: verificar que la llamada sea por AJAX solamente
    municipio_id = int( request.vars.dir_municipio_id )
    resultado = ''
    for c in comuna.obtener_comunas( municipio_id ):
        op = OPTION(c.nombre, _value=c.id)
        resultado += op.xml()
    return resultado

@auth.requires_membership('administrators')
def obtener_municipios():
    # TODO: verificar que la llamada sea por AJAX solamente
    provincia_id = int( request.vars.dir_provincia_id )
    resultado = ''
    for m in municipio.obtener_municipios( provincia_id ):
        op = OPTION( m.nombre,_value=m.id )
        resultado += op.xml()
    return resultado

@auth.requires_membership('administrators')
def iniciar_candidatura():
    if not request.args(0):
        redirect( URL( 'iniciar_candidatura',args=['1'] ) )
    form = None

    if request.args(0) == '1':
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
        form = SQLFORM.factory( db.persona,formstyle='bootstrap',submit_button=T( 'Siguiente' ) )
        if form.process().accepted:
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
            session.candidatura = { 'persona':p }
            redirect( URL( 'iniciar_candidatura',args=['2'] ) )
    elif request.args(0) == '2':
        # paso 2: datos de la candidatura
        db.candidatura.estudiante_id.readable = False
        db.candidatura.estudiante_id.writable = False
        db.candidatura.es_trabajador.default = False
        db.candidatura.profesion.show_if = (db.candidatura.es_trabajador==True)
        db.candidatura.nombre_trabajo.show_if = (db.candidatura.es_trabajador==True)
        if request.vars.es_trabajador:
            db.candidatura.profesion.requires = tools.requerido
            db.candidatura.nombre_trabajo.requires = tools.requerido
        form = SQLFORM( db.candidatura,formstyle='bootstrap',submit_button=T( 'Siguiente' ),table_name='candidatura' )
        if form.process().accepted:
            pass
    elif request.args(0) == '3':
        # paso 3: selección de las carreras
        pass

    return dict( sidenav=sidenav,form=form,step=request.args(0) )
