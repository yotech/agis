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
from applications.agis.modules.gui.carrera_uo import seleccionar_carrera

sidenav.append(
    [T('Escuela'), # Titulo del elemento
     URL('configurar_escuela'), # url para el enlace
     ['configurar_escuela'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Unidades organicas'), # Titulo del elemento
     URL('gestion_uo'), # url para el enlace
     ['gestion_uo'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Régimen a realizar en la UO'), # Titulo del elemento
     URL('asignar_regimen'), # url para el enlace
     ['asignar_regimen'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Carreras a impartir en las UO'), # Titulo del elemento
     URL('asignar_carrera'), # url para el enlace
     ['asignar_carrera'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Gestión de Años Académicos'), # Titulo del elemento
     URL('ano_academico'), # url para el enlace
     ['ano_academico'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Departamentos'), # Titulo del elemento
     URL('departamentos'), # url para el enlace
     ['departamentos'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Niveles Académicos'), # Titulo del elemento
     URL('nivel_academico'), # url para el enlace
     ['nivel_academico'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Asignaturas'), # Titulo del elemento
     URL('asignaturas'), # url para el enlace
     ['asignaturas'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Grupos de estudiantes'), # Titulo del elemento
     URL('grupos'), # url para el enlace
     ['grupos'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Planes Curriculares'), # Titulo del elemento
     URL('planes_curriculares'), # url para el enlace
     ['planes_curriculares','asignatura_por_plan'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Plazas a otorgar'), # Titulo del elemento
     URL('plazas_estudiantes'), # url para el enlace
     ['plazas_estudiantes'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Eventos'), # Titulo del elemento
     URL('eventos'), # url para el enlace
     ['eventos'],] # en funciones estará activo este item
)

migas.append(
    tools.split_drop_down(
        Storage(dict(url='#', texto=T('Configuración'))),
        [Storage(dict(url=URL('general','index'),
                      texto=T('General'))),
         Storage(dict(url=URL('instituto','index'),
                      texto=T('Instituto'))),
         Storage(dict(url=URL('infraestructura','index'),
                      texto=T('Infraestructura'))),
         Storage(dict(url=URL('appadmin','manage',args=['auth']),
                      texto=T('Seguridad'))),
         ]
        )
    )
migas.append(A(T('Instituto'), _href=URL('index')))

def index():
    redirect(URL('configurar_escuela'))
    return dict(message="hello from instituto.py")

@auth.requires_membership(myconf.take('roles.admin'))
def grupos():
    migas.append('Grupos de estudiantes')
    manejo = grupo.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def plazas_estudiantes_ajax():
    if request.ajax:
        c_id = int(request.vars.c)
        a_id = int(request.vars.a)
        r_id = int(request.vars.r)
        #print request.vars
        p = plazas.buscar_plazas(ano_academico_id=a_id,
                                 regimen_id=r_id,
                                 carrera_id=c_id)
        db.plazas.id.readable=False
        db.plazas.ano_academico_id.default = a_id
        db.plazas.ano_academico_id.readable=False
        db.plazas.ano_academico_id.writable=False
        db.plazas.regimen_id.default = r_id
        db.plazas.regimen_id.readable = False
        db.plazas.regimen_id.writable = False
        db.plazas.carrera_id.default = c_id
        db.plazas.carrera_id.readable = False
        db.plazas.carrera_id.writable = False
        if not p:
            db.plazas.insert()
            db.commit()
            p = plazas.buscar_plazas(ano_academico_id=a_id,
                                     regimen_id=r_id,
                                     carrera_id=c_id)
        form = SQLFORM(db.plazas, record=p,
                       formstyle="divs",
                       submit_button=T( 'Guardar' ))
        if form.process(dbio=False).accepted:
            necesarias = int(form.vars.necesarias)
            maximas = int(form.vars.maximas)
            media = float(form.vars.media)
            if necesarias > maximas:
                maximas=necesarias
                form.vars.maximas = necesarias
            p.update_record(necesarias=necesarias,
                           maximas=maximas,
                           media=media)
            db.commit()
            form = SQLFORM(db.plazas, record=p,
                           formstyle="divs",
                           submit_button=T( 'Guardar' ))
            response.flash = T('Cambios guardados')
            #redirect( request.env.http_web2py_component_location,client_side=True)
        return dict(form=form)
    else:
        raise HTTP(500)

@auth.requires_membership(myconf.take('roles.admin'))
def plazas_estudiantes():
    def enlaces_step2(fila):
        return A(SPAN('', _class='glyphicon glyphicon-hand-up'),
                 _title=T('Definir plazas para nuevos ingresos'),
                 _href=URL('instituto',
                           'plazas_estudiantes',
                           vars=dict(step=2,carrera_id=fila.carrera_uo.id)),
                 _class='btn btn-default')
    if not 'step' in request.vars:
        redirect(URL('plazas_estudiantes',vars=dict(step=1)))
    step=request.vars.step
    manejo = None
    if step=='1':
        migas.append(T('Plazas'))
        manejo=carrera_uo.obtener_selector(
            enlaces_a=[dict(header='',body=enlaces_step2)])
    elif step=='2':
        # mostrar por cada año academico los regimenes de la unidad organica
        # de la carrera seleccionada.
        carrera=carrera_uo.obtener_por_id(int(request.vars.carrera_id))
        a_academicos = db((db.ano_academico.id>0) &
                          (db.evento.ano_academico_id==db.ano_academico.id) &
                          ((db.evento.tipo=='1') & (db.evento.estado==True))
                         ).select(db.ano_academico.id,db.ano_academico.nombre)
        regimenes = regimen_uo.obtener_regimenes_por_unidad( carrera.carrera_uo.unidad_organica_id )
        if not a_academicos:
            session.flash=T('No se han definido los años académicos o no se ha asociado ninguno con un evento de tipo inscripción')
            redirect(URL('plazas_estudiantes',vars=dict(step=1)))
        if not regimenes:
            session.flash=T('No se han definido regímenes para la UO')
            redirect(URL('plazas_estudiantes',vars=dict(step=1)))
        migas.append(A(T('Plazas'), _href=URL('plazas_estudiantes')))
        migas.append(carrera.descripcion_carrera.nombre)
        return dict(sidenav=sidenav,
                    carrera=carrera,
                    step=step,
                    a_academicos=a_academicos,
                    regimenes=regimenes)
        pass

    return dict( sidenav=sidenav,manejo=manejo,step=step )

@auth.requires_membership(myconf.take('roles.admin'))
def nivel_academico():
    migas.append(T('Niveles académicos'))
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

    return dict(sidenav=sidenav,
        manejo=manejo,
        select_uo=select_uo,
        niveles=niveles)

@auth.requires_membership(myconf.take('roles.admin'))
def ano_academico():
    migas.append(T('Gestión de Años Académicos'))
    manejo = a_academico.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def asignaturas():
    migas.append(T('Asignaturas'))
    manejo = asignatura.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def asignatura_por_plan():
    context = Storage(dict(sidenav=sidenav))
    if not 'plan_curricular_id' in request.vars:
        raise HTTP(404)

    plan_curricular_id=int(request.vars.plan_curricular_id)
    context['plan'] = db.plan_curricular(plan_curricular_id)
    context['carrera'] = db.descripcion_carrera(db.carrera_uo(context['plan'].carrera_id).descripcion_id)
    context['manejo'] = asignatura_plan.obtener_manejo( plan_curricular_id )
    migas.append(A(T('Planes Curriculares'),
                   _href=URL('planes_curriculares', vars=request.vars)))
    migas.append(T('Asignaturas'))
    return context

@auth.requires_membership(myconf.take('roles.admin'))
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

@auth.requires_membership(myconf.take('roles.admin'))
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

    migas.append(A(T('Planes Curriculares'),
                   _href=URL('planes_curriculares')))
    context = Storage(dict(sidenav=sidenav))
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

@auth.requires_membership(myconf.take('roles.admin'))
def eventos():
    manejo = evento.obtener_manejo()
    response.view = "instituto/asignaturas.html"
    migas.append(T('Eventos'))
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def departamentos():
    migas.append(T('Departamentos'))
    manejo = dpto.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def configurar_escuela():
    """Presenta formulario con los datos de la escuela y su sede cetral"""
    migas.append(T('Escuela'))
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
    return dict(form_escuela=form_escuela,sidenav=sidenav)

@auth.requires_membership(myconf.take('roles.admin'))
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
    migas.append(T('Carreras a impartir en las UO'))
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
    return dict( sidenav=sidenav, select_uo=select_uo, manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def asignar_regimen():
    migas.append(T('Régimen a realizar en la UO'))
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
    return dict(sidenav=sidenav,manejo=manejo,select_uo=select_uo)

@auth.requires_membership(myconf.take('roles.admin'))
def gestion_uo():
    """Vista para la gestión de las unidades organicas"""
    migas.append(T('Unidades Orgánicas'))
    esc = escuela.obtener_escuela()
    manejo = unidad_organica.obtener_manejo(esc.id)
    return dict(manejo=manejo,sidenav=sidenav)
