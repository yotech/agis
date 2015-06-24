# -*- coding: utf-8 -*-
from applications.agis.modules.db import escuela
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import persona
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules.db import escuela_media
from applications.agis.modules.db import regimen_uo
from applications.agis.modules import tools

sidenav.append(
    [T('Listado de candidatos'), # Titulo del elemento
     URL('listar_candidatos'), # url para el enlace
     ['listar_candidatos'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Iniciar candidatura'), # Titulo del elemento
     URL('iniciar_candidatura'), # url para el enlace
     ['iniciar_candidatura'],] # en funciones estará activo este item
)


def index():
    redirect( URL( 'listar_candidatos' ) )
    return dict( message="hello from candidatura.py" )

@auth.requires_membership( 'administrators' )
def listar_candidatos():
    manejo = candidatura.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def obtener_comunas():
    if request.ajax:
        municipio_id = int( request.vars.dir_municipio_id )
        resultado = ''
        for c in comuna.obtener_comunas( municipio_id ):
            op = OPTION(c.nombre, _value=c.id)
            resultado += op.xml()
    else:
        raise HTTP(404)
    return resultado

@auth.requires_membership('administrators')
def obtener_municipios():
    if request.ajax:
        provincia_id = int( request.vars.dir_provincia_id )
        resultado = ''
        for m in municipio.obtener_municipios( provincia_id ):
            op = OPTION( m.nombre,_value=m.id )
            resultado += op.xml()
    else:
        raise HTTP(404)
    return resultado

@auth.requires_membership('administrators')
def actualizar_regimenes():
    if request.ajax:
        unidad_organica_id = int( request.vars.unidad_organica_id )
        resultado = ''
        for re in regimen_uo.obtener_regimenes( unidad_organica_id ):
            id, nombre = re # es una tupla de la forma (id, nombre_regimen)
            op = OPTION( nombre,_value=id )
            resultado += op.xml()
    else:
        raise HTTP(404)
    return resultado

@auth.requires_membership('administrators')
def obtener_escuelas_medias():
    if request.ajax:
        tipo_escuela_media_id = int( request.vars.tipo_escuela_media_id )
        resultado = ''
        for e in escuela_media.obtener_escuelas( tipo_escuela_media_id ):
            op = OPTION( e.nombre,_value=e.id )
            resultado += op.xml()
    else:
        raise HTTP(404)
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
        if not session.candidatura:
            raise HTTP(404)
        db.candidatura.estudiante_id.readable = False
        db.candidatura.estudiante_id.writable = False
        db.candidatura.es_trabajador.default = False
        db.candidatura.profesion.show_if = (db.candidatura.es_trabajador==True)
        db.candidatura.nombre_trabajo.show_if = (db.candidatura.es_trabajador==True)
        if request.vars.es_trabajador:
            db.candidatura.profesion.requires = tools.requerido
            db.candidatura.nombre_trabajo.requires = tools.requerido
        if request.vars.tipo_escuela_media_id:
            tipo_escuela_media_id = int(request.vars.tipo_escuela_media_id)
        else:
            pt_escuela = db( db.tipo_escuela_media.id > 0).select().first()
            tipo_escuela_media_id = pt_escuela.id
        db.candidatura.tipo_escuela_media_id.default = tipo_escuela_media_id
        db.candidatura.escuela_media_id.requires = IS_IN_SET(
            escuela_media.obtener_posibles(tipo_escuela_media_id),
            zero=None)
        if request.vars.unidad_organica_id:
            unidad_organica_id = request.vars.unidad_organica_id
        else:
            unidad_organica_id = ( escuela.obtener_sede_central() ).id
        db.candidatura.unidad_organica_id.default = unidad_organica_id
        db.candidatura.regimen_unidad_organica_id.requires = IS_IN_SET(
            regimen_uo.obtener_regimenes( unidad_organica_id ),zero=None
        )
        form = SQLFORM.factory( db.candidatura,formstyle='bootstrap',submit_button=T( 'Siguiente' ),table_name='candidatura' )
        if form.process(dbio=False).accepted:
            p = dict()
            p["es_trabajador"] = form.vars.es_trabajador
            if form.vars.es_trabajador:
                p["profesion"] = form.vars.profesion
                p["nombre_trabajo"] = form.vars.nombre_trabajo
            p["habilitacion"] = form.vars.habilitacion
            p["tipo_escuela_media_id"] = form.vars.tipo_escuela_media_id
            p["escuela_media_id"] = form.vars.escuela_media_id
            p["carrera_procedencia"] = form.vars.carrera_procedencia
            p["ano_graduacion"] = form.vars.ano_graduacion
            p["unidad_organica_id"] = form.vars.unidad_organica_id
            p["discapacidades"] = form.vars.discapacidades
            p["documentos"] = form.vars.documentos
            p["regimen_unidad_organica_id"] = form.vars.regimen_unidad_organica_id
            p["ano_academico_id"] = form.vars.ano_academico_id
            session.candidatura["candidato"] = p
            redirect( URL( 'iniciar_candidatura',args=['3'] ) )
    elif request.args(0) == '3':
        # paso 3: selección de las carreras
        if not session.candidatura:
            raise HTTP(404)
        unidad_organica_id = session.candidatura["candidato"]["unidad_organica_id"]
        candidato_carrera = db.Table( db,'candidato_carrera',
            Field( 'carrera1','reference carrera_uo' ),
            Field( 'carrera2','reference carrera_uo' ),
        )
        candidato_carrera.carrera1.label = T("1ra carrera")
        candidato_carrera.carrera2.label = T("2da carrera")
        candidato_carrera.carrera1.requires = IS_IN_SET(
            carrera_uo.obtener_carreras(unidad_organica_id),
            zero=None)
        candidato_carrera.carrera2.requires = IS_IN_SET(
            carrera_uo.obtener_carreras(unidad_organica_id),
            zero=None)
        form = SQLFORM.factory( candidato_carrera,formstyle='bootstrap',submit_button=T( 'Siguiente' ) )
        if form.process(dbio=False).accepted:
            # tomar todos los datos y agregarlos a la base de datos
            persona_id = db.persona.insert( **db.persona._filter_fields(session.candidatura["persona"]) )
            estudiante_id = db.estudiante.insert( persona_id=persona_id )
            session.candidatura["candidato"]["estudiante_id"] = estudiante_id
            candidatura_id = db.candidatura.insert( **db.candidatura._filter_fields(session.candidatura["candidato"]) )
            db.candidatura_carrera.insert( candidatura_id=candidatura_id,
                carrera_id=form.vars.carrera1,
                prioridad=1 )
            db.candidatura_carrera.insert( candidatura_id=candidatura_id,
                carrera_id=form.vars.carrera2,
                prioridad=2 )
            session.candidatura = None
            session.flash = T( "Candidatura procesada" )
            redirect( URL("iniciar_candidatura",args=[1]) )

    return dict( sidenav=sidenav,form=form,step=request.args(0) )
