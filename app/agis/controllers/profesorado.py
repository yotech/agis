# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules.db import persona
from applications.agis.modules.db import provincia
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules.db import profesor_asignatura
from applications.agis.modules.db import profesor
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import departamento
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import asignatura_plan
from applications.agis.modules.db import evento

from applications.agis.modules.gui import profesor as profesor_gui

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
def editar_profesor():
    """componente para editar los datos de un profesor AJAX"""
    if not request.vars.profesor_id:
        raise HTTP(404)
    docente = db.profesor(int(request.vars.profesor_id))
    if not docente:
        raise HTTP(404)
    context = Storage(dict(sidenav=sidenav))
    c, f = profesor_gui.form_editar_profesor(docente.id)
    if f.process().accepted:
        # TODO: si no es ajax no hacer esto
        response.flash = T('Cambios guardados')
        response.js = "jQuery('#%s').get(0).reload()" % request.cid
    context.componente = c
    return context


@auth.requires_membership('administrators')
def editar_docente():
    """Presenta los formularios para edición de los datos de un profesor"""
    context = Storage(dict(sidenav=sidenav))
    if not request.vars.profesor_id:
        raise HTTP(404)
    v_profesor = db.profesor(int(request.vars.profesor_id))
    if not v_profesor:
        raise HTTP(404)
    v_persona = db.persona(v_profesor.persona_id)
    context.profesor = v_profesor
    context.persona = v_persona
    return context

@auth.requires_membership('administrators')
def asignar_asignatura():
    """Asignación de asignaturas a un profesor"""
    # antes seleccionar año academico.
    # 1ro seleccionar profesor
    # 2do seleccionar carrera
    # 3ro seleccionar plan
    # 4to seleccionar asignatura y evento
    # guardar todo eso en la Asignación y crear los permisos necesarios
    # para el profesor.
    context = Storage(dict(sidenav=sidenav))
    context.asunto = T('Asignación de asignaturas')
    migas.append(T('Asignación de asignaturas'))

    if not request.vars.unidad_organica_id:
        return unidad_organica.seleccionar(context)
    else:
        context.unidad_organica = db.unidad_organica(
            int(request.vars.unidad_organica_id))

    if not request.vars.ano_academico_id:
        return ano_academico.seleccionar(context)
    else:
        context.ano_academico = db.ano_academico(
            int(request.vars.ano_academico_id))

    if not request.vars.departamento_id:
        return departamento.seleccionar(context)
    else:
        context.departamento = db.departamento(
            int(request.vars.departamento_id))

    if not request.vars.profesor_id:
        return profesor.seleccionar(context)
    else:
        context.profesor = db.profesor(
            int(request.vars.profesor_id))

    if not request.vars.carrera_uo_id:
        return carrera_uo.seleccionar(context)
    else:
        context.carrera_uo = db.carrera_uo(
            int(request.vars.carrera_uo_id))

    if not request.vars.plan_curricular_id:
        return plan_curricular.seleccionar(context)
    else:
        context.plan_curricular = db.plan_curricular(
            int(request.vars.plan_curricular_id))

    if not request.vars.asignatura_plan_id:
        return asignatura_plan.seleccionar(context)
    else:
        context.asignatura_plan = db.asignatura_plan(
            int(request.vars.asignatura_plan_id))

    # listo, se tienen todos lo datos, se puede mostrar ahora el formulario
    db.profesor_asignatura.ano_academico_id.default = context.ano_academico.id
    db.profesor_asignatura.ano_academico_id.writable = False
    db.profesor_asignatura.profesor_id.default = context.profesor.id
    db.profesor_asignatura.profesor_id.writable = False
    context.asignatura = db.asignatura(
        context.asignatura_plan.asignatura_id)
    db.profesor_asignatura.asignatura_id.default = context.asignatura.id
    db.profesor_asignatura.asignatura_id.writable = False
    db.profesor_asignatura.evento_id.requires = IS_IN_SET(
        evento.opciones_evento(context.ano_academico.id),
        zero=None
        )
    form = SQLFORM(db.profesor_asignatura, submit_button=T('Asignar'))
    if form.process().accepted:
        params = request.vars
        del params['asignatura_plan_id']
        session.flash = T("Asignación guardada")
        redirect(URL('asignar_asignatura', vars=params))
    context.manejo = form
    return dict( context )

@auth.requires_membership('administrators')
def listado_general():
    def _enlaces(fila):
        """Genera enlace a la asignación de asignaturas del profesor"""
        text1 = T('Asignaciones')
        text2 = T('Editar')
        # debug ----------------
        #from pprint import pprint
        #pprint(fila)
        # ----------------------
        p = None
        if 'view' in request.args:
            p = db.profesor(fila.id)
        else:
            p = db.profesor(fila.profesor.id)
        url1 = URL('asignaciones',vars=dict(profesor_id=p.id))
        url2 = URL('editar_docente',vars=dict(profesor_id=p.id))
        asig_link = A(SPAN('', _class="glyphicon glyphicon-tasks"),
                 _title=text1, _href=url1, _class="btn btn-default btn-sm")
        edit_link = A(SPAN('', _class="glyphicon glyphicon-edit"),
                 _title=text2, _href=url2, _class="btn btn-default btn-sm")
        return CAT(asig_link, edit_link)

    migas.append(T('Listado general'))
    context = Storage(dict(sidenav=sidenav))
    enlaces = [dict(header='', body=_enlaces)]
    if 'view' in request.args:
        context.profesor = db.profesor(int(request.args(2)))
    context.manejo = profesor.obtener_manejo(enlaces=enlaces, detalles=True)
    return context

@auth.requires_membership('administrators')
def mostrar_asinaciones():
    """Muestra el dialogo para las asignaciones de asignaturas"""
    context = Storage(dict())
    context.manejo = URL('asignaciones.load',vars=request.vars)
    response.title = T('Asignación de asignaturas')
    return context

@auth.requires_membership('administrators')
def asignaciones():
    """Muestra grid para manejar asignaciones de asignaturas a un profesor"""
    context = Storage(dict())
    if not request.vars.profesor_id:
        raise HTTP(404)
    context.profesor = db.profesor(int(request.vars.profesor_id))
    if not context.profesor:
        raise HTTP(404)

    if 'new' or 'edit' in request.args:
        #preparar el formulario
        db.profesor_asignatura.profesor_id.default = \
            context.profesor.id
        db.profesor_asignatura.profesor_id.writable = False
        # departamento
        dpto = db.departamento(context.profesor.departamento_id)
        # unidad organica
        uni = db.unidad_organica(dpto.unidad_organica_id)
        # fijar los años academicos solo a los disponibles en la UO
        a_aca = []
        for a in db(db.ano_academico.unidad_organica_id == uni.id).select():
            a_aca.append((a.id, a.nombre))
        db.profesor_asignatura.ano_academico_id.requires = \
            IS_IN_SET(a_aca, zero=None)
        # fijar que las asignaturas solo sean de carreras de la misma unidad
        # organica a la que pertenece el trabajador
    if not request.extension or request.extension == 'html':
        migas.append(T('Asignación de asignaturas'))
        p = db.persona(context.profesor.persona_id)
        context.asunto = profesor.profesor_grado_represent(
            context.profesor.grado, None) + \
            ' ' + p.nombre_completo
    context.manejo = tools.manejo_simple(db.profesor_asignatura,
        buscar=False,
        crear=False,
        campos=[db.profesor_asignatura.asignatura_id,
                db.profesor_asignatura.ano_academico_id,
                db.profesor_asignatura.evento_id,
                db.profesor_asignatura.estado,
                db.profesor_asignatura.es_jefe])
    return context

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
            db.commit()
            form.vars.persona_id = persona_id
            db.profesor.insert( **db.profesor._filter_fields( form.vars ) )
            session.persona = None
            session.flash = T( "Datos del profesor guardados" )
            redirect( URL( 'agregar_profesor',args=['1'] ) )
    return dict( sidenav=sidenav,form=form,step=step )
