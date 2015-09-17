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

from applications.agis.modules.gui.profesor import form_editar_profesor
from applications.agis.modules.gui.profesor import seleccionar_profesor
from applications.agis.modules.gui.ano_academico import seleccionar_ano
from applications.agis.modules.gui.asignatura_plan import seleccionar_asignatura

rol_admin = myconf.take('roles.admin')

menu_lateral.append(
    Accion('Listado general', URL('listado_general'), [rol_admin]),
    ['listado_general', 'editar_docente'])
menu_lateral.append(
    Accion('Agregar profesor', URL('agregar_profesor'), [rol_admin]),
    ['agregar_profesor'])
menu_lateral.append(
    Accion('Asignar asignatura', URL('asignar_asignatura'), [rol_admin]),
    ['asignar_asignatura'])
menu_migas.append(Accion('Recursos Humanos', URL(''), []))
menu_migas.append(Accion('Profesorado', URL('index'), [rol_admin]))

def index():
    redirect( URL( 'listado_general' ) )
    return dict(message="hello from profesorado.py")

@auth.requires_membership(rol_admin)
def editar_profesor():
    """componente para editar los datos de un profesor AJAX"""
    if not request.vars.profesor_id:
        raise HTTP(404)
    docente = db.profesor(int(request.vars.profesor_id))
    if not docente:
        raise HTTP(404)
    context = Storage(dict())
    db.profesor.persona_id.readable = False
    c, f = form_editar_profesor(docente.id)
    if f.process().accepted:
        # TODO: si no es ajax no hacer esto
        response.flash = T('Cambios guardados')
        response.js = "jQuery('#%s').get(0).reload()" % request.cid
    context.componente = c
    return context


@auth.requires_membership(rol_admin)
def editar_docente():
    """Presenta los formularios para edición de los datos de un profesor"""
    context = Storage(dict())
    if not request.vars.profesor_id:
        raise HTTP(404)
    v_profesor = db.profesor(int(request.vars.profesor_id))
    if not v_profesor:
        raise HTTP(404)
    v_persona = db.persona(v_profesor.persona_id)
    context.profesor = v_profesor
    context.persona = v_persona
    menu_migas.append(T("Editar profesor"))
    return context

@auth.requires_membership(rol_admin)
def asignar_asignatura():
    """Asignación de asignaturas a un profesor"""
    context = Storage(dict())
    context.asunto = T('Asignación de asignaturas')
    menu_migas.append(T('Asignación de asignaturas'))

    if not request.vars.profesor_id:
        context.asunto = T('Seleccione un docente')
        context.manejo = seleccionar_profesor()
        return context
    else:
        context.profesor = db.profesor(
            int(request.vars.profesor_id))

    p = db.persona(context.profesor.persona_id)
    if not p.user_id:
        # el profe no tiene un usuario asignado, debe crearse el mismo antes
        # de continuar.
        session.flash = T("""
            El profesor seleccionado no tiene asociado un usuario valido en el
            sistema.
            """)
        redirect(URL('editar_docente',
                     vars=dict(profesor_id=context.profesor.id)))
    # con el profesor seleccionado se tiene la UO y el DPTO al que pertenece
    dpto = db.departamento(context.profesor.departamento_id)
    context.unidad_organica = db.unidad_organica(dpto.unidad_organica_id)

    if not request.vars.ano_academico_id:
        context.asunto = T('Seleccione Año Académico')
        context.manejo = seleccionar_ano(
            unidad_organica_id=context.unidad_organica.id)
        return context
    else:
        context.ano_academico = db.ano_academico(
            int(request.vars.ano_academico_id))

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
        context.asunto = T('Seleccionar asignatura')
        l_a = profesor_asignatura.asignaturas_por_profesor(context.profesor.id)
        l_a = [a.id for a in l_a]
        context.manejo = seleccionar_asignatura(
            plan_id=context.plan_curricular.id,
            no_esta_en=l_a)
        return context
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
        u = db.auth_user(p.user_id)
        if form.vars.es_jefe:
            # agregar al profesor al grupo jefe de asignaturas
            jrol = db(
                    db.auth_group.role == myconf.take('roles.jasignatura')
                ).select().first()
            if not auth.has_membership(group_id=jrol.id, user_id=u.id):
                auth.add_membership(group_id=jrol.id, user_id=u.id)

        params = request.vars
        del params['asignatura_plan_id']
        session.flash = T("Asignación guardada")
        redirect(URL('asignar_asignatura', vars=params))
    context.manejo = form
    return dict( context )

@auth.requires_membership(rol_admin)
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

    menu_migas.append(T('Listado general'))
    context = Storage(dict())
    enlaces = [dict(header='', body=_enlaces)]
    if 'view' in request.args:
        context.profesor = db.profesor(int(request.args(2)))
    context.manejo = profesor.obtener_manejo(enlaces=enlaces, detalles=True)
    return context

@auth.requires_membership(rol_admin)
def mostrar_asinaciones():
    """Muestra el dialogo para las asignaciones de asignaturas"""
    context = Storage(dict())
    context.manejo = URL('asignaciones.load',vars=request.vars)
    response.title = T('Asignación de asignaturas')
    return context

@auth.requires_membership(rol_admin)
def asignaciones():
    """Muestra grid para manejar asignaciones de asignaturas a un profesor"""
    context = Storage(dict())
    if not request.vars.profesor_id:
        raise HTTP(404)
    context.profesor = db.profesor(int(request.vars.profesor_id))
    if not context.profesor:
        raise HTTP(404)

    if 'edit' in request.args:
        for f in db.profesor_asignatura:
            f.writable = False
        db.profesor_asignatura.es_jefe.writable = True
        db.profesor_asignatura.estado.writable = True
    if not request.extension or request.extension == 'html':
        menu_migas.append(T('Asignación de asignaturas'))
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

@auth.requires_membership(rol_admin)
def agregar_profesor():
    if not request.args(0):
        redirect( URL( 'agregar_profesor',args=['1'] ) )
    step = request.args(0)
    form = None
    menu_migas.append(T('Agregar profesor'))

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
    return dict( form=form,step=step )
