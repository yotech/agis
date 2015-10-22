# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules.db import escuela
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import persona
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules.db import escuela_media
from applications.agis.modules.db import regimen_uo
from applications.agis.modules.db import candidatura_carrera
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import evento
from applications.agis.modules.db import examen
from applications.agis.modules.db import asignatura_plan
from applications.agis.modules.db import aula
from applications.agis.modules.db import profesor
from applications.agis.modules.db import profesor_asignatura
from applications.agis.modules.db import plan_curricular
from applications.agis.modules.db import nota
from applications.agis.modules.db.examen_aula_estudiante \
    import distribuir_estudiantes
from applications.agis.modules.db.asignacion_carrera import asignarCarreras
from applications.agis.modules import tools
from applications.agis.modules.gui.unidad_organica import seleccionar_uo
from applications.agis.modules.gui.evento import seleccionar_evento
from applications.agis.modules.gui.regimen_uo import seleccionar_regimen
from applications.agis.modules.gui.nota import grid_asignar_nota
from applications.agis.modules.gui.nota import form_editar_nota
from applications.agis.modules.gui.candidatura import leyenda_candidatura
from applications.agis.modules.gui.persona import leyenda_persona
from applications.agis.modules.gui.mic import *

rol_admin = auth.has_membership(role=myconf.take('roles.admin'))
rol_profesor = auth.has_membership(role=myconf.take('roles.profesor'))
#rol_jasig = auth.has_membership(role=myconf.take('roles.jasignatura'))
rol_oexamen = auth.has_membership(role=myconf.take('roles.oexamen'))

menu_lateral.append(
    Accion(T('Listado'), URL('listar_candidatos'), rol_admin),
    ['listar_candidatos','editar_candidatura'])
menu_lateral.append(
    Accion(T('Iniciar candidatura'),
           URL('iniciar_candidatura'), rol_admin),
    ['iniciar_candidatura'])
menu_lateral.append(
    Accion(T('Exámenes de acceso'),
           URL('examen_acceso'),
           rol_admin or rol_profesor or rol_oexamen),
    ['examen_acceso','aulas_para_examen','estudiantes_examinar',
      'codigos_estudiantes','notas_examen'])
menu_lateral.append(
    Accion(T("Resultados por carrera"), URL('resultados_por_carrera'), rol_admin),
    ['resultados_por_carrera'])
menu_migas.append(Accion(T('Candidatos'), URL('index'), True))


@auth.requires_login()
def index():
    """Factoria de vistas para los diferentes tipos de usuarios"""
    if rol_profesor or rol_oexamen:
        redirect(URL('examen_acceso'))
    redirect( URL( 'listar_candidatos' ) )
    return dict( message="hello from candidatura.py" )

@auth.requires(rol_admin)
def aulas_para_examen():
    aula.definir_tabla()
    examen.definir_tabla()
    context = dict()
    if not request.vars.ex_id:
        raise HTTP(404)
    if not request.vars.evento_id:
        raise HTTP(404)
    if not request.vars.uo_id:
        raise HTTP(404)
    context['examen'] = db.examen(int(request.vars.ex_id))
    context['evento'] = db.evento(int(request.vars.evento_id))
    context['unidad_organica'] = db.unidad_organica(int(request.vars.uo_id))
    context['candidaturas'] = len(
        examen.obtener_candidaturas(context['examen'].id))
    db.examen_aula.id.readable = False
    db.examen_aula.examen_id.default = context['examen'].id
    db.examen_aula.examen_id.writable = False
    query = ((db.examen_aula.examen_id == context['examen'].id) &
             (db.aula.id == db.examen_aula.aula_id))
    # configurar las aulas posibles [https://github.com/yotech/agis/issues/82]:
    if 'new' in request.args:
        todas = db((db.aula.id > 0) &
                   (db.aula.disponible == True)).select(
                       db.aula.id, db.aula.nombre)
        usadas = db((db.aula.id == db.examen_aula.aula_id) &
                    (db.examen_aula.examen_id == context['examen'].id)
                   ).select(db.aula.id, db.aula.nombre)
        posibles = []
        # resta de ambas
        for a in todas:
            if a not in usadas:
                posibles.append(a)
        # configurar db.examen.aula_id
        posibles = [(a.id, a.nombre) for a in posibles]
        if not posibles:
            # si no hay aulas dispobibles notificarlo
            session.flash = T("No quedan aulas disponibles")
            redirect(URL('aulas_para_examen',
                         vars={'uo_id': context['unidad_organica'].id,
                               'evento_id': context['evento'].id,
                               'ex_id': context['examen'].id}))
        db.examen_aula.aula_id.requires = IS_IN_SET(posibles, zero=None)
    # --------------------------------------------------------------------------
    context['manejo'] = tools.manejo_simple(conjunto=query,
                                            editable=False,
                                            campos=[db.aula.nombre,
                                                    db.aula.capacidad])
    response.title = T('Asignación de aulas para examen')
    response.subtitle = examen.examen_format(context['examen'])
    # migas
    menu_migas.append(
        Accion(T('Exámenes de acceso'),
               URL('examen_acceso'), True))
    menu_migas.append(Accion(
        context['unidad_organica'].nombre,
        URL('examen_acceso',
            vars=dict(unidad_organica_id=context['unidad_organica'].id)),
        True, ))
    menu_migas.append(Accion(
        context['evento'].nombre,
        URL('examen_acceso', vars=dict(
            unidad_organica_id=context['unidad_organica'].id,
            evento_id=context['evento'].id)),
        True))
    menu_migas.append(T('Aulas: ') + examen.examen_format(context['examen']))
    return context


@auth.requires(rol_admin or rol_oexamen)
def codigos_estudiantes():
    context = Storage(dict(mensaje=''))
    response.context = context
    if not request.vars.examen_id:
        raise HTTP(404)
    examen_id = int(request.vars.examen_id)
    ex = db.examen(examen_id)
    if not ex:
        raise HTTP(404)
    context['examen'] = ex
    evento_id = ex.evento_id
    context['evento'] = db.evento(evento_id)
    ano_academico_id = context.evento.ano_academico_id
    context['ano_academico'] = db.ano_academico(ano_academico_id)
    unidad_organica_id = context.ano_academico.unidad_organica_id
    context['unidad_organica'] = db.unidad_organica(unidad_organica_id)
    context['escuela'] = escuela.obtener_escuela()
    response.title = T('Listado de códigos')
    response.subtitle = db.asignatura(ex.asignatura_id).nombre + ' - ' + \
        str(ex.fecha)

    cand_ids = examen.obtener_candidaturas(ex.id)
    est_ids = [db.candidatura(c.id).estudiante_id for c in cand_ids]
    per_ids = [db.estudiante(id).persona_id for id in est_ids]
    query = ((db.persona.id > 0) & (db.persona.id.belongs(per_ids)))
    exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
        csv=False, tsv_with_hidden_cols=False, tsv=False, json=False,
        PDF=(tools.ExporterPDF, 'PDF'))
    db.persona.uuid.readable = True
    db.persona.uuid.label = 'UUID'
    context['manejo'] = tools.manejo_simple(query,
                                            campos=[db.persona.nombre_completo,
                                                    db.persona.numero_identidad,
                                                    db.persona.uuid],
                                            editable=False,
                                            borrar=False,
                                            crear=False, csv=True,
                                            exportadores=exportadores)
    # migas
    menu_migas.append(
        Accion(T('Exámenes de acceso'),
               URL('examen_acceso'), True))
    menu_migas.append(Accion(
        context['unidad_organica'].nombre,
        URL('examen_acceso',
            vars=dict(unidad_organica_id=context['unidad_organica'].id)),
        True, ))
    menu_migas.append(Accion(
        context['evento'].nombre,
        URL('examen_acceso', vars=dict(
            unidad_organica_id=context['unidad_organica'].id,
            evento_id=context['evento'].id)),
        True))
    menu_migas.append(examen.examen_format(context['examen']))
    return dict(context=context)

@auth.requires(rol_admin or rol_profesor)
def notas_examen():
    context = Storage()
    if not request.vars.examen_id:
        raise HTTP(404)
    examen_id = int(request.vars.examen_id)
    ex = db.examen(examen_id)
    if not ex:
        raise HTTP(404)
    context.examen = ex
    context.evento = db.evento(ex.evento_id)
    context.ano_academico = db.ano_academico(context.evento.ano_academico_id)
    context.unidad_organica = db.unidad_organica(
        context.ano_academico.unidad_organica_id)
    context.escuela = escuela.obtener_escuela()

    if 'new' in request.args:
        if not request.vars.estudiante_id:
            raise HTTP(404)
        est = db.estudiante(int(request.vars.estudiante_id))
        # el componente que envuelve al formulario y el formulario en si
        c, f = form_editar_nota(ex, est)
        if f.process().accepted:
            session.flash = T('Nota actualizada')
            redirect(URL('notas_examen', vars=dict(examen_id=ex.id)))
        context.manejo = c
    else:
        context.manejo = grid_asignar_nota(ex)

    # migas
    menu_migas.append(
        Accion(T('Exámenes de acceso'),
               URL('examen_acceso'), True))
    menu_migas.append(Accion(
        context.unidad_organica.nombre,
        URL('examen_acceso',
            vars=dict(unidad_organica_id=context.unidad_organica.id)),
        True, ))
    menu_migas.append(Accion(
        context.evento.nombre,
        URL('examen_acceso', vars=dict(
            unidad_organica_id=context.unidad_organica.id,
            evento_id=context.evento.id)),
        True))
    menu_migas.append(examen.examen_format(context.examen))
    return context

@auth.requires(rol_admin or rol_oexamen)
def estudiantes_examinar():
    context = dict(mensaje='')
    if not request.vars.examen_id:
        raise HTTP(404)
    examen_id = int(request.vars.examen_id)
    ex = db.examen(examen_id)
    if not ex:
        raise HTTP(404)
    context['examen'] = ex
    evento_id = ex.evento_id
    context['evento'] = db.evento(evento_id)
    ano_academico_id = context['evento'].ano_academico_id
    context['ano_academico'] = db.ano_academico(ano_academico_id)
    unidad_organica_id = context['ano_academico'].unidad_organica_id
    context['unidad_organica'] = db.unidad_organica(unidad_organica_id)
    context['escuela'] = escuela.obtener_escuela()
    response.title = T('Estudiantes a examinar') + ' - '
    response.title += 'examen/' + T(examen.examen_tipo_represent(ex.tipo, None))
    response.subtitle = examen.examen_format(context['examen'])
    response.subtitle += ' - ' + str(ex.fecha)
    response.context = context
    if not ex.fecha or not ex.fecha:
        session.flash = T(
            'Faltan por definir la fecha o el período para el examen')
        redirect(URL('examen_acceso',
                    vars=dict(unidad_organica_id=unidad_organica_id,
                              evento_id=evento_id)))
    # mandar a distrubuir los estudiantes por aulas
    distribuir_estudiantes(examen_id)
    # comprobar que se distribuyeron, si no se logro emitir mensaje para que se
    # cambien las aulas, etc.
    if db(db.examen_aula_estudiante.examen_id == examen_id).count():
        # mostrar ahora el listado
        query = ((db.examen_aula_estudiante.examen_id == examen_id) &
            (db.estudiante.id == db.examen_aula_estudiante.estudiante_id) &
            (db.persona.id == db.estudiante.persona_id) &
            (db.candidatura.estudiante_id == \
                db.examen_aula_estudiante.estudiante_id))
        csv = rol_admin
        # --iss144: esconder todos los campos excepto los que se muestran
        # en la consulta.
        for fd in db.persona:
            fd.readable = False
        db.persona.nombre_completo.readable = True
        for fd in db.candidatura:
            fd.readable = False
        db.candidatura.numero_inscripcion.readable = True
        for fd in db.examen_aula_estudiante:
            fd.readable = False
        db.examen_aula_estudiante.aula_id.readable = True
        for fd in db.estudiante:
            fd.readable = False
        db.persona.nombre_completo.label = T('Nombre')
        # --iss144 ------------------------------------------------------------
        exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
                            csv=False, tsv_with_hidden_cols=False, tsv=False,
                            json=False, PDF=(tools.ExporterPDF, 'PDF'),
                            XLS=(candidatura.EAEXLS, 'XLS')
                           )
        co = CAT()
        t = T("Relación de estudiantes para el exámen %s por aulas",
              examen.examen_format(context['examen']))
        grid = tools.manejo_simple(query,
            campos=[db.candidatura.numero_inscripcion,
                    db.persona.nombre_completo,
                    db.examen_aula_estudiante.aula_id],
            editable=False,
            borrar=False,
            crear=False, csv=csv,
            buscar=True,
            exportadores=exportadores)
        co.append(DIV(DIV(t,_class="panel-heading"),
                      DIV(grid,_class="panel-body"),
                      _class="panel panel-default"))
        context['manejo'] = co
    else:
        # no se pudo hacer la distribución por alguna razón.
        session.flash = T('''
            No se pudieron distribuir los estudiantes por falta de espacio
            en las aulas definidas para el examen
        ''')
        redirect(URL('examen_acceso',
                     vars=dict(unidad_organica_id=unidad_organica_id,
                               evento_id=evento_id)))

    # migas
    menu_migas.append(
        Accion(T('Exámenes de acceso'),
               URL('examen_acceso'), True))
    menu_migas.append(Accion(
        context['unidad_organica'].nombre,
        URL('examen_acceso',
            vars=dict(unidad_organica_id=context['unidad_organica'].id)),
        True, ))
    menu_migas.append(Accion(
        context['evento'].nombre,
        URL('examen_acceso', vars=dict(
            unidad_organica_id=context['unidad_organica'].id,
            evento_id=context['evento'].id)),
        True))
    menu_migas.append(examen.examen_format(context['examen']))

    return context

@auth.requires(rol_admin or rol_oexamen)
def publicar_notas():
    context = dict(mensaje='')
    if not request.vars.examen_id:
        raise HTTP(404)
    examen_id = int(request.vars.examen_id)
    ex = db.examen(examen_id)
    if not ex:
        raise HTTP(404)
    context['examen'] = ex
    evento_id = ex.evento_id
    context['evento'] = db.evento(evento_id)
    ano_academico_id = context['evento'].ano_academico_id
    context['ano_academico'] = db.ano_academico(ano_academico_id)
    unidad_organica_id = context['ano_academico'].unidad_organica_id
    context['unidad_organica'] = db.unidad_organica(unidad_organica_id)
    context['escuela'] = escuela.obtener_escuela()
    response.title = T('Estudiantes a examinar') + ' - '
    response.title += 'examen/' + T(examen.examen_tipo_represent(ex.tipo, None))
    response.subtitle = examen.examen_format(context['examen'])
    response.subtitle += ' - ' + str(ex.fecha)
    response.context = context
    if not ex.fecha or not ex.fecha:
        session.flash = T(
            'Faltan por definir la fecha o el período para el examen')
        redirect(URL('examen_acceso',
                    vars=dict(unidad_organica_id=unidad_organica_id,
                              e_id=evento_id)))
    # mandar a distrubuir los estudiantes por aulas
    distribuir_estudiantes(examen_id)
    # comprobar que se distribuyeron, si no se logro emitir mensaje para que se
    # cambien las aulas, etc.
    if db(db.examen_aula_estudiante.examen_id == examen_id).count():
        # mostrar ahora el listado
        query = ((db.examen_aula_estudiante.examen_id == examen_id) &
            (db.estudiante.id == db.examen_aula_estudiante.estudiante_id) &
            (db.persona.id == db.estudiante.persona_id) &
            (db.candidatura.estudiante_id == \
                db.examen_aula_estudiante.estudiante_id) &
            (db.nota.estudiante_id == db.estudiante.id) &
            (db.nota.examen_id == db.examen_aula_estudiante.examen_id))
        csv = rol_admin
        exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
                            csv=False, tsv_with_hidden_cols=False, tsv=False,
                            json=False, PDF=(tools.ExporterPDF, 'PDF'),
                            XLS=(candidatura.PNXLS, 'XLS')
                           )
        context['manejo'] = tools.manejo_simple(query,
            campos=[db.candidatura.numero_inscripcion,
                    db.persona.nombre_completo,
                    db.nota.valor],
            editable=False,
            borrar=False,
            crear=False, csv=csv,
            exportadores=exportadores)
    else:
        # no se pudo hacer la distribución por alguna razón.
        session.flash = T('''
            No se pudieron distribuir los estudiantes por falta de espacio
            en las aulas definidas para el examen
        ''')
        redirect(URL('examen_acceso',
                     vars=dict(unidad_organica_id=unidad_organica_id,
                               e_id=evento_id)))

    # migas
    menu_migas.append(
        Accion(T('Exámenes de acceso'),
               URL('examen_acceso'), True))
    menu_migas.append(Accion(
        context['unidad_organica'].nombre,
        URL('examen_acceso',
            vars=dict(unidad_organica_id=context['unidad_organica'].id)),
        True, ))
    menu_migas.append(Accion(
        context['evento'].nombre,
        URL('examen_acceso', vars=dict(
            unidad_organica_id=context['unidad_organica'].id,
            evento_id=context['evento'].id)),
        True))
    menu_migas.append(examen.examen_format(context['examen']))

    return context

@auth.requires(rol_admin or rol_profesor or rol_oexamen)
def examen_acceso():
    """Gestión de examenes de acceso"""
    context = Storage(dict())
    # seleccionar unidad organica
    if not request.vars.unidad_organica_id:
        menu_migas.append(T('Exámenes de acceso'))
        context.asunto = T('Seleccione una Unidad Orgánica')
        response.title = escuela.obtener_escuela().nombre
        response.subtitle = T('Unidades Orgánicas')
        context.manejo = seleccionar_uo()
        return context
    else:
        menu_migas.append(Accion(
            T('Exámenes de acceso'),
            URL('examen_acceso'),
            rol_admin or rol_profesor or rol_oexamen))
        unidad_organica_id = int(request.vars.unidad_organica_id)
        context.unidad_organica = db.unidad_organica(unidad_organica_id)

    # --iss135: utilizar el selector de eventos -------------------------------
    if not request.vars.evento_id:
        # Paso 2 seleccionar evento de inscripción activo
        response.flash = CAT(T('Seleccione Evento de Inscripción para '),
            context['unidad_organica'].nombre)
        context.manejo = seleccionar_evento(
            unidad_organica_id=unidad_organica_id)
        response.title = context['unidad_organica'].nombre
        response.subtitle = T('Eventos de inscripción')
        menu_migas.append(context['unidad_organica'].nombre)
        return context
    else:
        # ya se escogió el evento
        evento_id = int(request.vars.evento_id)
        context.evento = db.evento(evento_id)
        menu_migas.append(Accion(context['unidad_organica'].nombre,
            URL('examen_acceso',
                vars={'unidad_organica_id': unidad_organica_id}),
            rol_admin or rol_profesor or rol_oexamen))
    # --iss135: ---------------------------------------------------------------
    menu_migas.append(context['evento'].nombre)
    db.examen.evento_id.default = context['evento'].id
    db.examen.evento_id.writable = False
    # obtener todas las candidaturas para el año académico del evento.
    candidaturas = candidatura.obtener_por(
        (db.candidatura.ano_academico_id == context['evento'].ano_academico_id) &
        (db.candidatura.estado_candidatura == '2') # inscrito
    )
    # todas las carreras para las candidaturas seleccionadas
    carreras_ids = candidatura_carrera.obtener_carreras( candidaturas )
    # buscar de las carreras solicitadas aquellas que tienen un plan curricular
    # activo.
    planes = plan_curricular.obtener_para_carreras( carreras_ids )
    asig_todas = asignatura_plan.asignaturas_por_planes( planes )
    asig = []
    if 'new' in request.args:
        # buscar las asignaturas que ya tienen algún evento
        asig_estan = db((db.asignatura.id == db.examen.asignatura_id) &
                        (db.examen.evento_id == context['evento'].id)
                       ).select(db.asignatura.id, db.asignatura.nombre)
        # restarlas de las asignaturas posibles.
        for a in asig_todas:
            if a not in asig_estan:
                asig.append(a)
    asig_set = [(i.id, i.nombre) for i in asig]
    if not asig_set and ('new' in request.args):
        session.flash = T('''
            No existen asignaturas que se puedan asociar al evento de
            inscripción o no se han registrado candidaturas para este evento.
        ''')
        redirect(URL('examen_acceso',
                     vars=dict(evento_id=context.evento.id,
                               unidad_organica_id=context.unidad_organica.id),))
    db.examen.asignatura_id.requires = [
        IS_IN_SET(asig_set, zero=None),
        examen.ExamenAsignaturaIdValidator()]
    db.examen.asignatura_id.widget = SQLFORM.widgets.options.widget
    db.examen.fecha.requires = IS_DATE_IN_RANGE(
        minimum=context['evento'].fecha_inicio,
        maximum=context['evento'].fecha_fin,
    )
    if 'edit' in request.args:
        db.examen.asignatura_id.writable = False
    db.examen.id.readable = False
    db.examen.tipo.default = '1'
    db.examen.tipo.writable = False
    def enlaces_aulas(fila):
        a = Accion('',
            URL('aulas_para_examen',
                        vars={'uo_id': context['unidad_organica'].id,
                                'evento_id': context['evento'].id,
                                'ex_id': fila.id}),
            (rol_admin or rol_oexamen),
            SPAN('', _class='glyphicon glyphicon-blackboard'),
            _class="btn btn-default",
            _title=T("Asignar aulas")
            )
        return a
    def listado_estudiantes(fila):
        url1 = URL('estudiantes_examinar', vars={'examen_id': fila.id})
        a1 = Accion('', url1, (rol_admin or rol_oexamen),
                    SPAN('', _class='glyphicon glyphicon-list-alt'),
                    _class="btn btn-default",
                    _title=T("Estudiantes a examinar"),)
        url2 = URL('codigos_estudiantes', vars={'examen_id': fila.id})
        a2 = Accion('', url2, (rol_admin or rol_oexamen),
                    SPAN('', _class='glyphicon glyphicon-barcode'),
                    _class="btn btn-default",
                    _title=T("Códigos de estudiantes"),)
        url3 = URL('notas_examen', vars={'examen_id': fila.id})
        a3 = Accion('', url3, (rol_admin or rol_profesor),
                    SPAN('', _class='glyphicon glyphicon-ok'),
                    _class="btn btn-default",
                    _title=T("Asignar notas"),)
        url4 = URL('publicar_notas', vars={'examen_id': fila.id})
        a4 = Accion('', url4, (rol_admin or rol_oexamen),
                    SPAN('', _class='glyphicon glyphicon-list'),
                    _class="btn btn-default",
                    _title=T("Publicar notas"),)
        return CAT(a1, ' ', a2, ' ', a3, ' ', a4)
    enlaces = [dict(header='',body=enlaces_aulas),
               dict(header='',body=listado_estudiantes)]
    query = ((db.examen.evento_id == context['evento'].id) &
        (db.examen.tipo=='1'))
    # -- iss120: si no es admin filtrar solo los examenes para asignaturas
    #            a las que fue asignado el profesor, j, asignatura u organizador
    if not auth.has_membership(myconf.take('roles.admin')):
        # buscar la persona que coincida con el usuario actual para obtener el
        # id del profesor.
        u = db.auth_user(auth.user.id)
        persona_id = u.persona.select().first()
        pro = profesor.persona_a_profesor(persona_id)
        # buscar las asignaturas asignadas a este profesor.
        asignadas = profesor_asignatura.asignaturas_por_profesor(pro.id)
        l_asig = [a.id for a in asignadas]
        query &= (db.examen.asignatura_id.belongs(l_asig))
    # -------------------------------------------------------------------------
    # iss123: quien puede agregar examenes
    crear = auth.has_membership(role=myconf.take('roles.admin'))
    # ------------------------------------
    context['manejo'] = tools.manejo_simple(conjunto=query,
        campos=[db.examen.asignatura_id,
                db.examen.fecha,
                db.examen.periodo],
        enlaces=enlaces,
        editable=(rol_admin or rol_oexamen),
        borrar=False,
        crear=crear)
    response.title = context['evento'].nombre
    response.subtitle = T("Examenes de acceso")
    return context

@auth.requires(rol_admin or rol_oexamen)
def listar_candidatos():
    def enlace_editar(fila):
        a = Accion('',
                   URL('editar_candidatura',
                       vars={'step':'1','c_id': fila.candidatura.id}),
                   rol_admin,
                   SPAN('', _class='glyphicon glyphicon-edit'),
                   _class="btn btn-default", _title=T("Editar")
                   )
        return a

    candidatura.definir_tabla()
    response.escuela = escuela.obtener_escuela()
    exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
                        csv=False, tsv_with_hidden_cols=False, tsv=False,
                        json=False, PDF=(tools.ExporterPDFLandscape, 'PDF'),
                        )
    response.title = T("Listado general")
    response.subtitle = T("candidaturas")
    exportar = rol_admin
    grid = candidatura.obtener_manejo(
        campos=[db.persona.numero_identidad,
               db.persona.nombre_completo,
               db.candidatura.ano_academico_id,
               db.candidatura.unidad_organica_id,
               db.candidatura.estado_candidatura,
               db.candidatura.numero_inscripcion,
               db.candidatura.id,
               db.persona.id,
               ],
        cabeceras={'persona.numero_identidad':T('DNI'),
                 'persona.nombre_completo':T('Nombre'),
                 'candidatura.numero_inscripcion':T('# Inscripción')},
        enlaces=[dict(header="",body=enlace_editar)],
        buscar=True,
        exportar=exportar,
        exportadores=exportadores,
        )
    leyenda = DIV(DIV(leyenda_persona(), _class="col-md-6"),
                  DIV(leyenda_candidatura(), _class="col-md-6"),
                  _class="row")
    row_grid = DIV(DIV(grid, _class="col-md-12"),_class="row")
    manejo = CAT(leyenda, row_grid)
    menu_migas.append(T('Listado'))
    return dict(manejo=manejo )

@auth.requires(rol_admin)
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

@auth.requires(rol_admin)
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

@auth.requires(rol_admin)
def editar_candidatura():
    if not 'c_id' in request.vars:
        raise HTTP(404)
    c_id = int(request.vars.c_id)
    if not 'step' in request.vars:
        redirect(URL('editar_candidatura', vars={'step': '1', 'c_id': c_id}))
    step = request.vars.step
    form = None

    menu_migas.append(
        Accion(T('Listado'),
               URL('listar_candidatos'),
               rol_admin))

    response.title = T("Editar candidatura")
    if step == '1':
        # paso 1: datos personales
        p = candidatura.obtener_persona(c_id)
        db.persona.lugar_nacimiento.widget = SQLFORM.widgets.autocomplete(
            request,
            db.comuna.nombre,id_field=db.comuna.id)
        if request.vars.email:
            db.persona.email.requires.append(IS_EMAIL())
            db.persona.email.requires.append(
                IS_NOT_IN_DB(db, 'persona.email'))
        else:
            db.persona.email.requires = None

        if request.vars.dir_provincia_id:
            dir_provincia_id = int(request.vars.dir_provincia_id)
        else:
            dir_provincia_id = p.dir_provincia_id
        municipios = municipio.obtener_posibles( dir_provincia_id )
        db.persona.dir_municipio_id.requires = IS_IN_SET( municipios,zero=None )

        if request.vars.dir_municipio_id:
            dir_municipio_id = int(request.vars.dir_municipio_id)
        else:
            dir_municipio_id = p.dir_municipio_id
        comunas = comuna.obtener_posibles( dir_municipio_id )
        db.persona.dir_comuna_id.requires = IS_IN_SET( comunas,zero=None )
        db.persona.id.readable = False
        form = SQLFORM(db.persona,record=p, submit_button=T( 'Siguiente' ))
        form.add_button(T('Saltar'),
            URL('editar_candidatura', vars={'step': '2', 'c_id': c_id}))
        response.subtitle = T("Datos personales")
        menu_migas.append(T("Datos personales"))
        if form.process().accepted:
            redirect(URL('editar_candidatura',
                vars={'step': '2', 'c_id': c_id}))
    elif step == '2':
        # paso 2: datos de la candidatura
        c = db.candidatura[c_id]
        db.candidatura.estudiante_id.readable = False
        db.candidatura.estudiante_id.writable = False
        db.candidatura.numero_inscripcion.readable=False
        db.candidatura.profesion.show_if = (db.candidatura.es_trabajador==True)
        db.candidatura.nombre_trabajo.show_if = (
            db.candidatura.es_trabajador==True)
        if request.vars.es_trabajador:
            db.candidatura.profesion.requires = [
                IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
            db.candidatura.nombre_trabajo.requires = [
                IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        if request.vars.tipo_escuela_media_id:
            tipo_escuela_media_id = int(request.vars.tipo_escuela_media_id)
        else:
            tipo_escuela_media_id = c.tipo_escuela_media_id
        db.candidatura.tipo_escuela_media_id.default = tipo_escuela_media_id
        db.candidatura.escuela_media_id.requires = IS_IN_SET(
            escuela_media.obtener_posibles(tipo_escuela_media_id),
            zero=None)
        if request.vars.unidad_organica_id:
            unidad_organica_id = request.vars.unidad_organica_id
        else:
            unidad_organica_id = c.unidad_organica_id
        db.candidatura.unidad_organica_id.default = unidad_organica_id
        db.candidatura.regimen_unidad_organica_id.requires = IS_IN_SET(
            regimen_uo.obtener_regimenes( unidad_organica_id ),zero=None
        )
        db.candidatura.id.readable=False
        form = SQLFORM(db.candidatura,
                       record=c,
                       submit_button=T( 'Siguiente' ))
        form.add_button(T('Saltar'),
            URL('editar_candidatura', vars={'step': '3', 'c_id': c_id}))
        response.subtitle = T("Datos candidatura")
        menu_migas.append(T("Datos candidatura"))
        if form.process().accepted:
            redirect(URL('editar_candidatura',
                vars={'step': '3', 'c_id': c_id}))
    elif step == '3':
        c = db.candidatura[c_id]
        unidad_organica_id = c.unidad_organica_id
        db.candidatura_carrera.carrera_id.requires = IS_IN_SET(
            carrera_uo.obtener_carreras(unidad_organica_id),
            zero=None)
        response.subtitle = T("Selección de carrera")
        menu_migas.append(T("Selección de carrera"))
        form = candidatura_carrera.obtener_manejo(c_id)

    return dict(form=form,step=step)

@auth.requires(rol_admin)
def iniciar_candidatura():
    if not request.args(0):
        redirect( URL( 'iniciar_candidatura',args=['1'] ) )
    step = request.args(0)
    form = None

    menu_migas.append(
        Accion(T('Iniciar candidatura'),
               URL('iniciar_candidatura'),
               rol_admin))

    if step == '1':
        # paso 1: datos personales
        db.persona.lugar_nacimiento.widget = SQLFORM.widgets.autocomplete(
            request,
            db.comuna.nombre,id_field=db.comuna.id)
        if request.vars.email:
            db.persona.email.requires.append(IS_EMAIL())
            db.persona.email.requires.append(
                IS_NOT_IN_DB(db, 'persona.email'))
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
        db.persona.dir_municipio_id.requires = IS_IN_SET(municipios,zero=None)
        comunas = comuna.obtener_posibles( dir_municipio_id )
        db.persona.dir_comuna_id.requires = IS_IN_SET( comunas,zero=None )
        f = SQLFORM.factory(db.persona, submit_button=T( 'Siguiente' ))
        menu_migas.append(T('Datos personales'))
        if f.process().accepted:
            ## guardar los datos de persona y pasar el siguiente paso
            p = dict(nombre=f.vars.nombre,
                apellido1=f.vars.apellido1,
                apellido2=f.vars.apellido2,
                fecha_nacimiento=f.vars.fecha_nacimiento,
                genero=f.vars.genero,
                lugar_nacimiento=f.vars.lugar_nacimiento,
                estado_civil=f.vars.estado_civil,
                tipo_documento_identidad_id=f.vars.tipo_documento_identidad_id,
                numero_identidad=f.vars.numero_identidad,
                nombre_padre=f.vars.nombre_padre,
                nombre_madre=f.vars.nombre_madre,
                estado_politico=f.vars.estado_politico,
                nacionalidad=f.vars.nacionalidad,
                dir_provincia_id=f.vars.dir_provincia_id,
                dir_municipio_id=f.vars.dir_municipio_id,
                dir_comuna_id=f.vars.dir_comuna_id,
                direccion=f.vars.direccion,
                telefono=f.vars.telefono,
                email=f.vars.email
            )
            session.candidatura = { 'persona':p }
            redirect( URL( 'iniciar_candidatura',args=['2'] ) )
        form=CAT()
        header = DIV('Datos personales', _class="panel-heading")
        body = DIV(f, _class="panel-body")
        form.append(DIV(header, body, _class="panel panel-default"))
    elif step == '2':
        # paso 2: datos de la candidatura
        if not session.candidatura:
            raise HTTP(404)
        menu_migas.append(T('Datos candidatura'))
        db.candidatura.estudiante_id.readable = False
        db.candidatura.estudiante_id.writable = False
        db.candidatura.numero_inscripcion.readable=False
        db.candidatura.es_trabajador.default = False
        db.candidatura.profesion.show_if = (db.candidatura.es_trabajador==True)
        db.candidatura.nombre_trabajo.show_if = (db.candidatura.es_trabajador==True)
        if request.vars.es_trabajador:
            db.candidatura.profesion.requires.append(IS_NOT_EMPTY(error_message=current.T('Información requerida')))
            db.candidatura.nombre_trabajo.requires.append(IS_NOT_EMPTY(error_message=current.T('Información requerida')))
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
        f = SQLFORM.factory( db.candidatura, submit_button=T( 'Siguiente' ),table_name='candidatura' )
        if f.process(dbio=False).accepted:
            p = dict()
            p["es_trabajador"] = f.vars.es_trabajador
            if f.vars.es_trabajador:
                p["profesion"] = f.vars.profesion
                p["nombre_trabajo"] = f.vars.nombre_trabajo
            p["habilitacion"] = f.vars.habilitacion
            p["tipo_escuela_media_id"] = f.vars.tipo_escuela_media_id
            p["escuela_media_id"] = f.vars.escuela_media_id
            p["carrera_procedencia"] = f.vars.carrera_procedencia
            p["ano_graduacion"] = f.vars.ano_graduacion
            p["unidad_organica_id"] = f.vars.unidad_organica_id
            p["discapacidades"] = f.vars.discapacidades
            p["documentos"] = f.vars.documentos
            p["regimen_unidad_organica_id"] = f.vars.regimen_unidad_organica_id
            p["ano_academico_id"] = f.vars.ano_academico_id
            session.candidatura["candidato"] = p
            redirect( URL( 'iniciar_candidatura',args=['3'] ) )
        form=CAT()
        header = DIV('Datos candidatura', _class="panel-heading")
        body = DIV(f, _class="panel-body")
        form.append(DIV(header, body, _class="panel panel-default"))
    elif step == '3':
        # paso 3: selección de las carreras
        menu_migas.append(T('Carreras'))
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
        f = SQLFORM.factory(candidato_carrera,
                               submit_button=T( 'Siguiente' ))
        if f.process(dbio=False).accepted:
            # tomar todos los datos y agregarlos a la base de datos
            persona_id = db.persona.insert( **db.persona._filter_fields(session.candidatura["persona"]) )
            estudiante_id = db.estudiante.insert( persona_id=persona_id )
            session.candidatura["candidato"]["estudiante_id"] = estudiante_id
            candidatura_id = db.candidatura.insert( **db.candidatura._filter_fields(session.candidatura["candidato"]) )
            db.candidatura_carrera.insert( candidatura_id=candidatura_id,
                carrera_id=f.vars.carrera1,
                prioridad=1 )
            db.candidatura_carrera.insert( candidatura_id=candidatura_id,
                carrera_id=f.vars.carrera2,
                prioridad=2 )
            session.candidatura = None
            session.flash = T( "Candidatura procesada" )
            redirect( URL("iniciar_candidatura",args=[1]) )
        form=CAT()
        header = DIV('Opciones de carreras', _class="panel-heading")
        body = DIV(f, _class="panel-body")
        form.append(DIV(header, body, _class="panel panel-default"))

    return dict(form=form,step=step )

@auth.requires(rol_admin)
def resultados_por_carrera():
    context = Storage()
    menu_migas.append(Accion(T('Resultados'),
        URL('resultados_por_carrera'), True))
    menu_migas.append(T('Carrera'))
    if not request.vars.unidad_organica_id:
        context.manejo = seleccionar_uo()
        return context
    else:
        unidad_organica_id = int(request.vars.unidad_organica_id)

    if not request.vars.regimen_unidad_organica_id:
        context.manejo = seleccionar_regimen(unidad_organica_id)
        return context
    else:
        regimen_id = int(request.vars.regimen_unidad_organica_id)

    if not request.vars.evento_id:
        context.manejo = seleccionar_evento(
            unidad_organica_id=unidad_organica_id)
        return context
    else:
        evento_id = int(request.vars.evento_id)
        ano_academico_id = db.evento(evento_id).ano_academico_id

    # obtener todas las candidaturas para el año académico del evento.
    candidaturas = candidatura.obtener_por(
        (db.candidatura.ano_academico_id == ano_academico_id) &
        (db.candidatura.estado_candidatura != candidatura.INSCRITO_CON_DEUDAS )
    )
    # todas las carreras para las candidaturas seleccionadas
    carreras_ids = candidatura_carrera.obtener_carreras(candidaturas)
    if not request.vars.carrera_uo_id:
        co = CAT()
        query = (db.carrera_uo.id > 0)
        query &= (db.carrera_uo.unidad_organica_id == unidad_organica_id)
        query &= (db.carrera_uo.descripcion_id == db.descripcion_carrera.id)
        query &= (db.carrera_uo.id.belongs(carreras_ids))
        grid = tools.selector(query,
            [db.carrera_uo.id, db.descripcion_carrera.nombre],
            'carrera_uo_id', tabla='carrera_uo')
        heading = DIV(T('Seleccionar carrera'), _class="panel-heading")
        body = DIV(grid, _class="panel-body")
        panel = DIV(heading, body, _class="panel panel-default")
        co.append(panel)
        context.manejo = co
        return context
    else:
        carrera_uo_id = int(request.vars.carrera_uo_id)

    # realizar asignaciones de carreras
    #realizarAsignacion(carrera_uo_id, evento_id, regimen_id)
    asignarCarreras(evento_id, regimen_id)

    # ahora buscar todas las candidaturas que hayan seleccionado en alguna
    # opción la carrera que no es lo mismo que la lista anterior.
    candidaturas = candidatura_carrera.obtenerCandidaturasPorCarrera(
        carrera_uo_id, ano_academico_id=ano_academico_id,
        unidad_organica_id=unidad_organica_id)
    cand_ids = [r.id for r in candidaturas]
    query = ((db.persona.id == db.estudiante.persona_id) &
             (db.candidatura.estudiante_id == db.estudiante.id))
    query &= (db.candidatura.estado_candidatura.belongs(
        [candidatura.NO_ADMITIDO, candidatura.ADMITIDO]))
    query &= (db.candidatura.regimen_unidad_organica_id == regimen_id)
    query &= (db.candidatura.id.belongs(cand_ids))
    # buscar las asignaturas para las que es necesario hacer examen de
    # acceso para la carrera.
    asig_set = plan_curricular.obtenerAsignaturasAcceso(carrera_uo_id)
    def notasEnGrid(row):
        p = db.persona(row.persona.id)
        est = db.estudiante(uuid=p.uuid)
        ex_ids = [db.examen(asignatura_id=a, evento_id=evento_id) for a in asig_set]
        cantidad = len(ex_ids)
        suma = 0
        tabla = TABLE()
        heading = TR()
        for a_id in asig_set:
            a = db.asignatura(a_id)
            heading.append(TH(a.abreviatura))
        heading.append(TH(T("Media")))
        vals = TR()
        for ex in ex_ids:
            if ex:
                n = db.nota(examen_id=ex.id, estudiante_id=est.id)
                vals.append(TD(nota.nota_format(n)))
                if n and n.valor != None:
                    suma += n.valor
            else:
                vals.append(TD('0'))
        vals.append(TD("%.2f" % (float(suma)/cantidad, )))
        tabla.append(heading)
        tabla.append(vals)
        return tabla
    enlaces = [dict(header='',body=notasEnGrid)]
    db.persona.nombre_completo.label = T("Nombre")
    db.candidatura.numero_inscripcion.label = T("# Inscripción")
    # configurar campos
    db.persona.id.readable = False
    db.persona.nombre.readable = False
    db.persona.apellido1.readable = False
    db.persona.apellido2.readable = False
    for f in db.estudiante:
        f.readable = False
    db.candidatura.ano_academico_id.readable = False
    db.candidatura.unidad_organica_id.readable = False
    db.candidatura.estudiante_id.readable = False
    db.candidatura.id.readable = False
    heading = DIV(
        T("Resultados para %s" % (carrera_uo.carrera_uo_format(
            db.carrera_uo(carrera_uo_id)),)),
        _class="panel-heading")
    exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
        csv=False, tsv_with_hidden_cols=False, tsv=False,
        json=False, PDF=(tools.ExporterPDFLandscape, 'PDF'),
        XLS=(candidatura.ResultadosPorCarreraXLS, 'XLS'),
    )
    campos = [db.persona.nombre_completo,
                db.candidatura.numero_inscripcion,
                db.candidatura.estado_candidatura]
    if request.vars._export_type:
        # estamos exportando a algún formato, incluir todo en response
        campos.append(db.persona.id)
        context.unidad_organica_id = unidad_organica_id
        context.ano_academico_id = ano_academico_id
        context.evento_id = evento_id
        context.carrera_uo_id = carrera_uo_id
        response.context = context
    body = DIV(SQLFORM.grid(query=query,
        fields=campos, links=enlaces,
        searchable=True, create=False, editable=False, csv=True,
        details=False, deletable=False, showbuttontext=False,
        exportclasses=exportadores),
        _class="panel-body")
    context.manejo = DIV(heading, body,_class="panel panel-default")

    return context
