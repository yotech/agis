# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import escuela
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import regimen_uo
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import ano_academico as a_academico
from applications.agis.modules.db import departamento as dpto
from applications.agis.modules.db import nivel_academico as nivel
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import plan_curricular
from applications.agis.modules.db import plazas
from applications.agis.modules.db import evento
from applications.agis.modules.db import asignatura_plan
from applications.agis.modules.db import grupo
from applications.agis.modules.gui.unidad_organica import seleccionar_uo
from applications.agis.modules.gui.ano_academico import seleccionar_ano
from applications.agis.modules.gui.regimen_uo import seleccionar_regimen
from applications.agis.modules.gui.carrera_uo import seleccionar_carrera

rol_admin = auth.has_membership(role=myconf.take('roles.admin'))

menu_lateral.append(
    Accion('Escuela', URL('configurar_escuela'), rol_admin),
    ['configurar_escuela'])
menu_lateral.append(
    Accion('Unidades organicas',
           URL('gestion_uo'), rol_admin),
    ['gestion_uo'])
menu_lateral.append(
    Accion('Régimen a realizar en la UO',
           URL('asignar_regimen'), rol_admin),
    ['asignar_regimen'])
menu_lateral.append(
    Accion('Carreras a impartir en las UO',
           URL('asignar_carrera'),
           rol_admin),
    ['asignar_carrera'])
menu_lateral.append(
    Accion('Gestión de Años Académicos',
           URL('ano_academico'),
           rol_admin),
    ['ano_academico'])
menu_lateral.append(
    Accion('Departamentos',
           URL('departamentos'),
           rol_admin),
    ['departamentos'])
menu_lateral.append(
    Accion('Niveles Académicos',
           URL('nivel_academico'),
           rol_admin),
    ['nivel_academico'])
menu_lateral.append(
    Accion('Asignaturas', URL('asignaturas'), rol_admin),
    ['asignaturas'])
menu_lateral.append(
    Accion('Grupos de estudiantes',
           URL('grupos'),
           rol_admin),
    ['grupos'])
menu_lateral.append(
    Accion('Planes Curriculares',
           URL('planes_curriculares'), rol_admin),
    ['planes_curriculares'])
menu_lateral.append(
    Accion('Plazas a otorgar',
           URL('plazas_estudiantes'), rol_admin),
    ['plazas_estudiantes'])
menu_lateral.append(
    Accion('Eventos', URL('eventos'), rol_admin),
    ['eventos'])


menu_migas.append(Accion('Configuración', '#', True))
menu_migas.append(
    Accion('Instituto', URL('index'), rol_admin))

def index():
    redirect(URL('configurar_escuela'))
    return dict(message="hello from instituto.py")

@auth.requires(rol_admin)
def grupos():
    menu_migas.append(T('Grupos de estudiantes'))
    manejo = grupo.obtener_manejo()
    return dict(manejo=manejo)

@auth.requires(rol_admin)
def plazas_estudiantes():
    context = Storage()
    menu_migas.append(
        Accion(T('Plazas nuevo ingreso'),
               URL('plazas_estudiantes'),
               True))
    if not request.vars.unidad_organica_id:
        context.manejo = seleccionar_uo()
        return context
    else:
        unidad_organica_id = int(request.vars.unidad_organica_id)
        menu_migas.append(
            Accion(db.unidad_organica(unidad_organica_id).abreviatura,
                URL('plazas_estudiantes',
                    vars=dict(unidad_organica_id=unidad_organica_id)),
                True))

    if not request.vars.ano_academico_id:
        context.manejo = seleccionar_ano(unidad_organica_id=unidad_organica_id)
        return context
    else:
        ano_academico_id = int(request.vars.ano_academico_id)
        menu_migas.append(
            Accion(db.ano_academico(ano_academico_id).nombre,
                URL('plazas_estudiantes',
                    vars=dict(unidad_organica_id=unidad_organica_id,
                              ano_academico_id=ano_academico_id)),
                True))

    if not request.vars.regimen_unidad_organica_id:
        context.manejo = seleccionar_regimen(unidad_organica_id)
        return context
    else:
        regimen_unidad_organica_id = int(
            request.vars.regimen_unidad_organica_id)
        menu_migas.append(
            Accion(regimen_uo.regimen_unidad_organica_format(
                    db.regimen_unidad_organica(regimen_unidad_organica_id)),
                URL('plazas_estudiantes',
                    vars=dict(unidad_organica_id=unidad_organica_id,
                              ano_academico_id=ano_academico_id)),
                True))

    db.plazas.ano_academico_id.default = ano_academico_id
    db.plazas.regimen_id.default = regimen_unidad_organica_id
    db.plazas.ano_academico_id.writable = False
    db.plazas.regimen_id.writable = False
    db.plazas.ano_academico_id.readable = False
    db.plazas.regimen_id.readable = False
    # generar para cada carrera asociada a la unidad organica
    q = (db.carrera_uo.id > 0)
    q &= (db.carrera_uo.unidad_organica_id == unidad_organica_id)
    for c in db(q).select():
        plazas.buscar_plazas(carrera_id=c.id,
            ano_academico_id=ano_academico_id,
            regimen_id=regimen_unidad_organica_id)
    co = CAT()
    panel = DIV(_class="panel panel-default")
    header = DIV(T("Gestión de plazas a otorgar"), _class="panel-heading")
    body = DIV(_class="panel-body")
    co.append(panel)
    panel.append(header)
    panel.append(body)
    q = (db.plazas.id > 0)
    q &= (db.plazas.ano_academico_id == ano_academico_id)
    q &= (db.plazas.regimen_id == regimen_unidad_organica_id)
    # config db.plazas
    db.plazas.id.readable = False
    if 'edit' in request.args:
        db.plazas.carrera_id.writable = False
    grid = tools.manejo_simple(q, crear=False)
    body.append(grid) # grid
    context.manejo = co

    return context

@auth.requires(rol_admin)
def nivel_academico():
    menu_migas.append(T('Niveles académicos'))
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    niveles = []
    for n in nivel.obtener_niveles(unidad_organica_id):
        niveles.append(n.nivel)
    manejo = SQLFORM.factory(
        Field('niveles','list:integer'), submit_button=T( 'Guardar' ),
        #formstyle="bootstrap",
    )
    if manejo.process().accepted:
        lista = manejo.vars.niveles
        parsed_lista = [int(x) for x in lista]
        nivel.actualizar_niveles(parsed_lista, unidad_organica_id)
        session.flash = T('Cambios guardados')
        redirect(URL(c=request.controller,
            f=request.function,
            vars={'unidad_organica_id':unidad_organica_id}))

    return dict(manejo=manejo, select_uo=select_uo, niveles=niveles)

@auth.requires(rol_admin)
def ano_academico():
    menu_migas.append(T('Gestión de Años Académicos'))
    manejo = a_academico.obtener_manejo()
    return dict(manejo=manejo)

@auth.requires(rol_admin)
def asignaturas():
    menu_migas.append(T('Asignaturas'))
    manejo = asignatura.obtener_manejo()
    return dict(manejo=manejo )

@auth.requires(rol_admin)
def asignatura_por_plan():
    context = Storage(dict())
    if not 'plan_curricular_id' in request.vars:
        raise HTTP(404)

    plan_curricular_id=int(request.vars.plan_curricular_id)
    context['plan'] = db.plan_curricular(plan_curricular_id)
    context['carrera'] = db.descripcion_carrera(db.carrera_uo(context['plan'].carrera_id).descripcion_id)
    context['manejo'] = asignatura_plan.obtener_manejo( plan_curricular_id )
    menu_migas.append(
        Accion('Planes Curriculares',
               URL('planes_curriculares', vars=request.vars),
               [myconf.take('roles.admin')]))
    menu_migas.append(T('Asignaturas'))
    return context

@auth.requires(rol_admin)
def activar_plan():
    if 'plan_curricular_id' in request.vars:
        plan_curricular_id=int(request.vars.plan_curricular_id)
    else:
        raise HTTP( 404 )
    plan = db.plan_curricular[plan_curricular_id]
    q = ((db.plan_curricular.id > 0) &
         (db.plan_curricular.carrera_id==plan.carrera_id))
    db(q).update(estado=False)
    db.commit()
    plan.update_record(estado=True)
    db.commit()
    redirect(URL('planes_curriculares',
                vars=request.vars))

@auth.requires(rol_admin)
def planes_curriculares():
    # TODO: se debe reimplementar completo
    def manejo_carrera_planes(plan):
        param = request.vars
        param.plan_curricular_id = plan.id
        return A(T('Gestionar'),
                 _href=URL('asignatura_por_plan',
                           vars=param) )
    def enlace_activar(plan):
        param = request.vars
        param.plan_curricular_id = plan.id
        if plan.estado:
            return ''
        else:
            return A(T('Activar'),
                _href=URL('activar_plan', vars=param))

    menu_migas.append(
        Accion('Planes Curriculares', URL('planes_curriculares'),
               [myconf.take('roles.admin')]))
    context = Storage(dict())
    context.asunto = None

    if not request.vars.unidad_organica_id:
        context.asunto = T('Seleccione la Unidad Orgánica')
        context.manejo = seleccionar_uo()
        response.title = T('Unidades orgánicas')
        return context
    else:
        context.unidad_organica = db.unidad_organica(
            int(request.vars.unidad_organica_id))

    if not request.vars.carrera_uo_id:
        context.asunto = T('Seleccione la carrera')
        response.title = context.unidad_organica.nombre + ' - ' + T('Carreras')
        response.subtitle = T('Carreras')
        context.manejo = seleccionar_carrera(
            unidad_organica_id=context.unidad_organica.id)
        return context
    else:
        context.carrera_uo = db.carrera_uo(
            int(request.vars.carrera_uo_id))

    context.descrip = db.descripcion_carrera(context.carrera_uo.descripcion_id)
    enlaces=[dict(header='', body=manejo_carrera_planes),
    dict(header='', body=enlace_activar)]
    db.plan_curricular.carrera_id.default = context.carrera_uo.id
    db.plan_curricular.carrera_id.readable = False
    db.plan_curricular.carrera_id.writable = False
    db.plan_curricular.estado.writable = False
    context.asunto = context.descrip.nombre + ' - ' + T('Planes Curriculares')
    context.manejo = plan_curricular.obtener_manejo(enlaces=enlaces,
        carrera_id=context.carrera_uo.id)

    return context

@auth.requires(rol_admin)
def eventos():
    co = CAT()
    response.view = "instituto/asignaturas.html"
    heading = DIV(_class="panel-heading")
    body = DIV(_class="panel-body")
    co.append(DIV(heading, body, _class="panel panel-default"))
    if not request.vars.unidad_organica_id:
        grid = seleccionar_uo()
        heading.append(T("Seleccione la Unidad Orgánica"))
        body.append(grid)
        return dict(manejo=co)
    else:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    heading.append(T("Gestión de eventos"))
    manejo = evento.obtener_manejo(unidad_organica_id)
    body.append(manejo)
    menu_migas.append(T('Eventos'))
    return dict(manejo=co)

@auth.requires(rol_admin)
def departamentos():
    menu_migas.append(T('Departamentos'))
    manejo = dpto.obtener_manejo()
    return dict(manejo=manejo )

@auth.requires(rol_admin)
def configurar_escuela():
    """Presenta formulario con los datos de la escuela y su sede cetral"""
    menu_migas.append(T('Escuela'))
    instituto = escuela.obtener_escuela()
    db.escuela.id.readable = False
    db.escuela.id.writable = False

    form_escuela = SQLFORM(db.escuela,instituto,
                           #formstyle='bootstrap',
                           upload=URL('default','download'))
    response.title = T("Configurar escuela")
    if form_escuela.process(dbio=False).accepted:
        form_escuela.vars.codigo=escuela.calcular_codigo_escuela( db.escuela._filter_fields( form_escuela.vars ) )
        db( db.escuela.id==instituto.id ).update( **db.escuela._filter_fields( form_escuela.vars ) )
        db.commit()
        unidad_organica.actualizar_codigos()
        session.flash = T( "Cambios guardados" )
        redirect('configurar_escuela')
    return dict(form_escuela=form_escuela)

@auth.requires(rol_admin)
def asignar_carrera():
    """
    Permite asignarle carreras a las unidades organicas
    """
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    menu_migas.append(T('Carreras a impartir en las UO'))
    db.carrera_uo.unidad_organica_id.default = unidad_organica_id
    db.carrera_uo.unidad_organica_id.writable = False
    db.carrera_uo.unidad_organica_id.readable = False
    db.carrera_uo.id.readable = False
    db.carrera_uo.id.writable = False
    query = ( db.carrera_uo.unidad_organica_id == unidad_organica_id )
    if 'new' in request.args:
        # preparar para agregar un nuevo elemento
        posibles_carreras = carrera_uo.obtener_posibles(unidad_organica_id)
        if posibles_carreras:
            db.carrera_uo.descripcion_id.requires = IS_IN_SET( posibles_carreras, zero=None )
        else:
            session.flash = T("Ya se han asociados todas las posibles carreras a la UO")
            redirect(URL('asignar_carrera',vars={'unidad_organica_id': unidad_organica_id}))
    manejo = tools.manejo_simple( query,editable=False )
    return dict(select_uo=select_uo, manejo=manejo )

@auth.requires(rol_admin)
def asignar_regimen():
    menu_migas.append(T('Régimen a realizar en la UO'))
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    db.regimen_unidad_organica.unidad_organica_id.default = unidad_organica_id
    db.regimen_unidad_organica.unidad_organica_id.writable = False
    db.regimen_unidad_organica.id.readable = False
    query = (db.regimen_unidad_organica.unidad_organica_id ==  unidad_organica_id)
    if 'new' in request.args:
        # preparar para agregar un nuevo elemento
        posibles_regimenes = regimen_uo.obtener_posibles_en_instituto(unidad_organica_id)
        if posibles_regimenes:
            db.regimen_unidad_organica.regimen_id.requires = IS_IN_SET( posibles_regimenes, zero=None )
        else:
            session.flash = T("Ya se han asociados todos los posibles regímenes a la UO")
            redirect(URL('asignar_regimen',vars={'unidad_organica_id': unidad_organica_id}))
    manejo = tools.manejo_simple(query,editable=False)
    return dict(manejo=manejo,select_uo=select_uo)

@auth.requires(rol_admin)
def gestion_uo():
    """Vista para la gestión de las unidades organicas"""
    menu_migas.append(T('Unidades Orgánicas'))
    esc = escuela.obtener_escuela()
    manejo = unidad_organica.obtener_manejo(esc.id)
    return dict(manejo=manejo)
