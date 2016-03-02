# -*- coding: utf-8 -*-

if False:
    from gluon import *
    from db import *
    from menu import *
    from tables import *
    from gluon.contrib.appconfig import AppConfig
    from gluon.tools import Auth, Service, PluginManager
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = DAL('sqlite://storage.sqlite')
    myconf = AppConfig(reload=True)
    auth = Auth(db)
    service = Service()
    plugins = PluginManager()
    from agiscore.gui.mic import MenuLateral, MenuMigas
    menu_lateral = MenuLateral(list())
    menu_migas = MenuMigas()

import datetime
from gluon.storage import Storage
from agiscore.gui.mic import Accion, grid_simple
# from agiscore.db.evento import evento_tipo_represent
from agiscore.gui.persona import form_crear_persona_ex
from agiscore.gui.evento import form_configurar_evento
from agiscore.db.examen import generar_examenes_acceso_ex
from agiscore.db.evento import esta_activo
from agiscore.db.nivel_academico import ACCESO
from agiscore.validators import IS_DATE_LT
from agiscore import tools
from datetime import date

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Registro de candidatos'),
                           URL('candidaturas', args=[request.args(0)]),
                           True),
                    ['candidaturas', 'inscribir',
                     'pago_inscripcion', 'editar'])
menu_lateral.append(Accion(T('Configurar evento'),
                           URL('configurar', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin'))),
                    ['configurar'])
menu_lateral.append(Accion(T('Plazas'),
                           URL('plazas', args=[request.args(0)]),
                           True),
                    ['plazas'])
menu_lateral.append(Accion(T('Asignación Docentes'),
                           URL('asignaciones', args=[request.args(0)]),
                           True),
                    ['asignaciones'])
menu_lateral.append(Accion(T('Examenes de acceso'),
                           URL('examenes', args=[request.args(0)]),
                           auth.has_membership(role=myconf.take('roles.admin')) or
                           auth.has_membership(role=myconf.take('roles.profesor'))),
                    ['examenes'])
menu_lateral.append(Accion(T('Resultados por carrera'),
                           URL('resultados_carrera', args=[request.args(0)]),
                           True),
                    ['resultados_carrera'])
menu_lateral.append(Accion(T('Candidaturas por carrera'),
                           URL('candidatos_carreras', args=[request.args(0)]),
                           True),
                    ['candidatos_carreras'])


@auth.requires_login()
def index():
    """UI evento de inscripción"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    redirect(URL("candidaturas", args=[C.evento.id]))
    
    return dict(C=C)

@auth.requires_login()
def resultados_carrera():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Resultados por carrera"))
    
    if request.args(1) is None:
        # Mostrar las carreras para que se seleccionen
        tbl = db.carrera_uo
        query = (tbl.id > 0) & (tbl.unidad_organica_id == C.unidad.id)
        text_lengths = {'carrera_uo.carrera_escuela_id': 60, }
        # query &= (tbl.carrera_escuela_id == db.carrera_escuela.id)
        # query &= (db.carrera_escuela.descripcion_id ==  db.descripcion_carrera.id)
        campos = [tbl.id, tbl.carrera_escuela_id]
        
        def _links(row):
            co = CAT()
            url = URL("resultados_carrera", args=[request.args(0), row.id])
            
            co.append(Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                                 ' ',
                                 T("Resultados")),
                             url,
                             True,
                             _class="btn btn-default btn-sm"))
            return co
        enlaces = [dict(header="", body=_links)]
        C.titulo = T("Carreras - {}".format(C.unidad.nombre))
        
        C.grid = grid_simple(query,
                             fields=campos,
                             args=request.args[:1],
                             links=enlaces,
                             create=False,
                             editable=False,
                             deletable=False,
                             maxtextlengths=text_lengths,
                             searchable=False,
                             history=False)
        return dict(C=C)
    else:
        C.carrera = db.carrera_uo(int(request.args(1)))
     
    from agiscore.db import candidatura_carrera
    from agiscore.db import candidatura
    candidaturas = candidatura_carrera.obtenerCandidaturasPorCarrera(
        C.carrera.id, ano_academico_id=C.ano.id,
        unidad_organica_id=C.unidad.id)
    cand_ids = [r.id for r in candidaturas]
    query = ((db.persona.id == db.estudiante.persona_id) & 
             (db.candidatura.estudiante_id == db.estudiante.id))
    query &= (db.candidatura.estado_candidatura.belongs(
        [candidatura.NO_ADMITIDO, candidatura.ADMITIDO]))
#     query &= (db.candidatura.regimen_unidad_organica_id == regimen_id)
    query &= (db.candidatura.id.belongs(cand_ids))
    # # configurar campos
    for f in db.persona:
        f.readable = False
    db.persona.nombre_completo.readable = True
    db.persona.nombre_completo.label = T("Nombre")
    for f in db.estudiante:
        f.readable = False
    for f in db.candidatura:
        f.readable = False
#     db.candidatura.estado_candidatura.readable = True
    db.candidatura.numero_inscripcion.readable = True
    db.candidatura.regimen_id.readable = True
    grid = SQLFORM.grid(query,
                        searchable=True,
                        create=False,
                        paginate=False,
                        args=request.args[:2])
    C.grid = grid
    # buscar las asignaturas para las que es necesario hacer examen de
    # acceso para la carrera.
    from agiscore.db import plan_curricular, nota
#     asig_set = plan_curricular.obtenerAsignaturasAcceso(C.carrera.id)
    plan_c = db.plan_curricular(carrera_id=C.carrera.id, estado=True)
    q_asig = (db.asignatura_plan.plan_curricular_id == plan_c.id)
    q_asig &= (db.asignatura_plan.nivel_academico_id == db.nivel_academico.id)
    q_asig &= (db.nivel_academico.nivel == ACCESO)
    asig_set = db(q_asig).select(db.asignatura_plan.ALL,
                                 cache=(current.cache.ram, 300),
                                 cacheable=True)
    
    filas = grid.rows
    # construir una lista con todos los datos de cada candidato que se usaran.
    todos = list()
    for row in filas:
        p = db.persona(row.persona.id)
        est = db.estudiante(uuid=p.uuid)
        item = Storage()
        item.ninscripcion = row.candidatura.numero_inscripcion
        item.nombre = row.persona.nombre_completo
        reg = db.regimen_unidad_organica(row.candidatura.regimen_id)
        item.regimen = db.regimen(reg.regimen_id).abreviatura
        item.media = nota.obtenerResultadosAcceso(row.candidatura.id,
                                                  C.carrera.id, C.evento.id)
        item.notas = list()
        for a in asig_set:
            ex = db.examen(asignatura_id=a.asignatura_id,
                           evento_id=C.evento.id)
            n = db.nota(examen_id=ex.id, estudiante_id=est.id)
            if n:
                if n.valor is not None:
                    item.notas.append(n.valor)
                else:
                    item.notas.append(0)
            else:
                item.notas.append(0)
        admi = db.asignacion_carrera(carrera_id=C.carrera.id, candidatura_id=row.candidatura.id)
        if admi:
            item.estado = T('ADMITIDO')
        else:
            item.estado = T('NO ADMITIDO')
        todos.append(item)
    # ordenar todos por la media.
    if not request.vars.order:
        todos.sort(cmp=lambda x, y: cmp(y.media, x.media))
    elif request.vars.order == "persona.nombre_completo":
        todos.sort(cmp=lambda x, y: cmp(x.nombre, y.nombre))
    if request.vars.myexport:
        response.context = C
        C.asignaturas = asig_set
        if request.vars.myexport == 'PDF':
            # si es PDF, hacer las cosas del PDF
            filename = "resultados_por_carrera.pdf"
            response.headers['Content-Type'] = "application/pdf"
            response.headers['Content-Disposition'] = \
                'attachment;filename=' + filename + ';'
            pdf = tools.MyFPDF()
            pdf.alias_nb_pages()
            pdf.add_page('')
            pdf.set_font('dejavu', '', 12)
            html = response.render("inscripcion/resultados_por_carrera.pdf",
                                dict(rows=todos,
                                    asignaturas=asig_set))
            pdf.write_html(html)
            raise HTTP(200, XML(pdf.output(dest='S')), **response.headers)
        elif request.vars.myexport == 'XLS':
            # si es XLS otras cosas
            eX = candidatura.ResultadosPorCarreraXLS(todos)
            response.headers['Content-Type'] = eX.content_type
            response.headers['Content-Disposition'] = \
                'attachment;filename=' + eX.file_name + '.' + eX.file_ext + ';'
            raise HTTP(200, XML(eX.export()), **response.headers)
    html = response.render("inscripcion/resultados_por_carrera_master.html",
        dict(rows=todos, asignaturas=asig_set))
    from agiscore.db import carrera_uo
    C.titulo = T("Resultados para %s" % (carrera_uo.carrera_uo_format(
             db.carrera_uo(C.carrera.id)),))
    contenido = CAT()
    # TODO: si cambian la implementación de SQLFORM.grid estamos jodios
    contenido.append(grid.components[0])
    contenido.append(XML(html))
    # contenido.append(DIV(busqueda[1]))
    C.grid = contenido


    
    return dict(C=C)

@auth.requires_login()
def candidatos_carreras():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Candidaturas por carreras"))
   
    # -- preparar el grid
    tbl = db.candidatura
    
    # -- configurar consulta
    query = (tbl.id > 0)
    query &= (tbl.ano_academico_id == C.ano.id)
    query &= (tbl.estudiante_id == db.estudiante.id)
    query &= (db.estudiante.persona_id == db.persona.id)
    query &= (db.candidatura_carrera.candidatura_id == tbl.id)
    
    exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
        csv=False, tsv_with_hidden_cols=False, tsv=False, json=False,
        PDF=(tools.ExporterPDF, 'PDF'))
    
    # -- configuración de los campos
    campos = [tbl.id,
              tbl.numero_inscripcion,
              db.persona.nombre_completo,
              tbl.regimen_id,
              db.candidatura_carrera.carrera_id,
              db.candidatura_carrera.prioridad]
    tbl.id.readable = False
    tbl.estudiante_id.readable = False
    db.estudiante.id.readable = False
    db.estudiante.persona_id.readable = False
    db.persona.id.readable = False
    db.persona.nombre_completo.label = T("Nombre")
    tbl.numero_inscripcion.label = T("# Ins.")
    db.candidatura_carrera.id.readable = False
    db.candidatura_carrera.candidatura_id.readable = False
    tbl.regimen_id.represent = lambda id, r: \
        db.regimen(db.regimen_unidad_organica(id).regimen_id).abreviatura
    
    text_lengths = {'persona.nombre_completo': 45,
                    'candidatura_carrera.carrera_id': 50}
    
    if request.vars._export_type:
        response.context = C

    C.grid = grid_simple(query,
                         create=False,
                         editable=False,
                         history=False,
                         csv=True,
                         sortable=True,
                         fields=campos,
                         deletable=False,
                         maxtextlengths=text_lengths,
                         exportclasses=exportadores,
                         orderby=[db.persona.nombre_completo, db.candidatura_carrera.prioridad],
                         args=request.args[:1])

    return dict(C=C)

@auth.requires_login()
def plazas():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Plazas por carrera"))
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # -- predeterminar/crear registros por defecto para cada carrera y regimen
    if puede_crear:
        r_q = (db.regimen_unidad_organica.id > 0) 
        r_q &= (db.regimen_unidad_organica.unidad_organica_id == C.unidad.id)
        
        c_q = (db.carrera_uo.id > 0)
        c_q &= (db.carrera_uo.unidad_organica_id == C.unidad.id)
        from agiscore.db.plazas import buscar_plazas
        for r in db(r_q).select():
            for c in db(c_q).select():
                buscar_plazas(C.ano.id, r.id, c.id)
    
    tbl = db.plazas
    query = (tbl.id > 0) & (tbl.ano_academico_id == C.ano.id)
    
    tbl.id.readable = False
    tbl.ano_academico_id.readable = False
    tbl.ano_academico_id.writable = False
    tbl.regimen_id.writable = False
    tbl.carrera_id.writable = False
    tbl.necesarias.label = T('Necesarias')
    tbl.maximas.label = T('Máximas')
    
    text_lengths = {'plazas.carrera_id': 50, }
    
    C.grid = grid_simple(query,
                         create=False,
                         editable=puede_editar,
                         deletable=False,
                         maxtextlengths=text_lengths,
                         orderby=[tbl.regimen_id, tbl.carrera_id],
                         args=request.args[:1])
    
    return dict(C=C)

@auth.requires_login()
def asignaciones():
    '''Asignación de las asignaturas a los profesores para la calificación
    de los examenes'''
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Asignación de asignaturas"))
    
    # permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin'))
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # crear un grid para la asignación de las asignaturas a los profesores
    C.titulo = T("Asignaciones de asignaturas")
    tbl = db.profesor_asignatura
    
    query = (tbl.id > 0) & (tbl.evento_id == C.evento.id)
    
    tbl.id.readable = False
    tbl.evento_id.default = C.evento.id
    tbl.evento_id.readable = False
    tbl.evento_id.writable = False
    
    if 'new' in request.args:
        a_set = (db.asignatura.id > 0) 
        a_set &= (db.asignatura.id == db.examen.asignatura_id)
        a_set &= (db.examen.evento_id == C.evento.id)
        tbl.asignatura_id.requires = IS_IN_DB(db(a_set),
                                              db.asignatura.id,
                                              "%(nombre)s",
                                              zero=None)
        p_set = (db.profesor.id > 0)
        p_set &= (db.profesor.departamento_id == db.departamento.id)
        p_set &= (db.departamento.unidad_organica_id == C.unidad.id)
        p_set &= (db.profesor.persona_id == db.persona.id)
        posibles = [(p.profesor.id, p.persona.nombre_completo) for p in \
                    db(p_set).select(orderby=db.persona.nombre_completo)]
        tbl.profesor_id.requires = IS_IN_SET(posibles, zero=None)
    campos = [tbl.id, tbl.profesor_id, tbl.asignatura_id,
              tbl.estado, tbl.es_jefe]
    tbl.es_jefe.label = T("Jefe")
    
    text_lengths = {'profesor_asignatura.asignatura_id': 50,
                    'profesor_asignatura.profesor_id': 50}
    
    C.grid = grid_simple(query,
                         create=puede_crear,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         maxtextlengths=text_lengths,
                         fields=campos,
                         args=request.args[:1])
    
    return dict(C=C)

@auth.requires_login()
def examenes():
    '''Examenes'''
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Examenes de acceso"))
    
    # permisos
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # si el evento esta activo generar los examenes pertinentes
    if esta_activo(C.evento):
        # generar los examenes de acceso
        generar_examenes_acceso_ex(C.evento, db)
    
    # -- recoger los examenes
    tbl = db.examen
    query = (tbl.id > 0) & (tbl.evento_id == C.evento.id)
    
    # configurar campos
    tbl.id.readable = False
    tbl.evento_id.readable = False
    tbl.tipo.readable = False
    
    if 'edit' in request.args:
        tbl.asignatura_id.readable = False
        tbl.asignatura_id.writable = False
        tbl.evento_id.writable = False
        tbl.tipo.writable = False
        
        tbl.inicio.label = T('Inicio')
        tbl.fin.label = T('Finalización')
        tbl.inicio.comment = T('''
            Hora de inicio en el formato HH:MM:SS
        ''')
        tbl.fin.comment = T('''
            Hora de terminación en el formato HH:MM:SS
        ''')
        tbl.fecha.requires = IS_DATE_IN_RANGE(minimum=C.evento.fecha_inicio,
                                              maximum=C.evento.fecha_fin)
    
    if 'view' in request.args:
        redirect(URL('examen', 'index', args=[request.args(3)]))
    
    text_lengths = {'examen.asignatura_id': 50}
    
    C.grid = grid_simple(query,
                         create=False,
                         editable=puede_editar,
                         deletable=puede_borrar,
                         maxtextlengths=text_lengths,
                         details=True,
                         searchable=False,
                         args=request.args[:1])
        
    return dict(C=C)

# TODO: añadir demás roles
@auth.requires(auth.has_membership(role=myconf.take('roles.admin')) or
               auth.has_membership(role=myconf.take('roles.incribidor')))
def inscribir():
    '''Proceso de inscripción'''
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Inscripción"))
    
    # -- cancelar
    mi_vars = Storage(request.vars)  # make a copy
    mi_vars._formulario_inscribir = 1
    cancelar = URL(c=request.controller, f=request.function,
                   args=request.args, vars=mi_vars)
    if request.vars._formulario_inscribir:
        session.q2Wh = None
        redirect(URL('candidaturas', args=[C.evento.id])) 
    # inicialización del formulario
    if session.q2Wh is None:
        session.q2Wh = Storage(dict(step=0))
        session.q2Wh.estudiante = Storage()
        session.q2Wh.candidatura = Storage()
    data = session.q2Wh
    
    back = URL('candidaturas', args=[C.evento.id])
    # -- recoger los datos personales
    if session.q2Wh.persona is None:
        (C.form_persona, pdata) = form_crear_persona_ex(cancel_url=back,
                                               db=db,
                                               T=T,
                                               session=session,
                                               request=request)
        if pdata is None:
            return dict(C=C)
        session.q2Wh.persona = pdata
        C.form_persona = None
    
    if data.step == 0:
        # -- recoger los datos del estudiante
        fld_habilitacion = db.estudiante.get('pro_habilitacion')
        fld_tipo_escuela = db.estudiante.get('pro_tipo_escuela')
        fld_pro_carrera = db.estudiante.get('pro_carrera')
        fld_pro_carrera.comment = T('''
            Nombre de la carrera que concluyó en la enseñanza previa
        ''')
        fld_pro_ano = db.estudiante.get('pro_ano')
        fld_pro_ano.comment = T('''
            Año en que se gradúo en la enseñanza media
        ''')
        fld_pro_ano.requires = IS_IN_SET(range(1950, date.today().year + 1),
                                         zero=None)
        fld_pro_ano.default = date.today().year - 1
        
        C.form = SQLFORM.factory(fld_habilitacion,
                                 fld_tipo_escuela,
                                 fld_pro_carrera,
                                 fld_pro_ano,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        C.form.add_button("Cancel", cancelar)
        C.titulo = T("Procedencia 1/2")
        if C.form.process().accepted:
            session.q2Wh.estudiante.update(C.form.vars)
            session.q2Wh.step = 1
            redirect(URL('inscribir', args=[C.evento.id]))
            
        return dict(C=C)
    
    if data.step == 1:
        # --segunda parte de los datos de procedencia
        C.titulo = T("Procedencia 2/2")
        
        # -- configurar campos
        campos = []
        tipo_escuela_id = int(data.estudiante.pro_tipo_escuela)
        tipo_escuela = db.tipo_escuela_media(tipo_escuela_id)
        if tipo_escuela.uuid != "a57d6b2b-8f0e-4962-a2a6-95f5c82e015d":
            fld_pro_escuela = db.estudiante.get("pro_escuela_id")
            esc_set = (db.escuela_media.id > 0)
            esc_set &= (db.escuela_media.tipo_escuela_media_id == tipo_escuela_id)
            fld_pro_escuela.requires = IS_IN_DB(db(esc_set),
                                                db.escuela_media.id,
                                                '%(nombre)s',
                                                zero=None)
            campos.append(fld_pro_escuela)
        fld_pro_media = db.estudiante.get("pro_media")
        campos.append(fld_pro_media)
        fld_es_trab = Field('es_trab', 'string', length=1, default='Não')
        fld_es_trab.label = T('¿Es trabajador?')
        fld_es_trab.requires = IS_IN_SET(['Sim', 'Não'], zero=None)
        campos.append(fld_es_trab)
        
        C.form = SQLFORM.factory(*campos,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        C.form.add_button("Cancel", cancelar)
        
        if C.form.process().accepted:
            vals = C.form.vars
            vals.es_trabajador = False if vals.es_trab == 'Não' else True
            session.q2Wh.estudiante.update(vals)
            session.q2Wh.step = 2
            redirect(URL('inscribir', args=[C.evento.id]))
        return dict(C=C)
    
    if data.step == 2:
        if data.estudiante.es_trabajador:
            # --pedir los datos del centro de trabajo
            C.titulo = T("Información laboral 1/2")
            fld_trab_profesion = db.estudiante.get('trab_profesion')
            fld_trab_profesion.requires = [IS_NOT_EMPTY(), IS_UPPER()]
            fld_trab_nombre = db.estudiante.get("trab_nombre")
            fld_trab_nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
            fld_trab_provincia = db.estudiante.get("trab_provincia")
            fld_trab_provincia.label = T("Provincia")
            fld_trab_provincia.comment = T('''
                Seleccione la provincia donde se desempeña el trabajo
            ''')
            fld_trab_provincia.requires = IS_IN_DB(db, db.provincia.id,
                                                   "%(nombre)s",
                                                   zero=None)
            fld_trab_tipo_instituto = db.estudiante.get('trab_tipo_instituto')
            from agiscore.db.estudiante import TRAB_TIPO_INSTITUTO
            fld_trab_tipo_instituto.requires = IS_IN_SET(TRAB_TIPO_INSTITUTO,
                                                         zero=None)
            fld_trab_con_titulo = Field('con_titulo', 'string', length=3,
                                        default='Não')
            fld_trab_con_titulo.label = T("¿Tiene salida con título?")
            fld_trab_con_titulo.requires = IS_IN_SET(['Sim', 'Não'], zero=None)
            
            C.form = SQLFORM.factory(fld_trab_profesion,
                                     fld_trab_nombre,
                                     fld_trab_tipo_instituto,
                                     fld_trab_con_titulo,
                                     fld_trab_provincia,
                                     table_name="estudiante",
                                     submit_button=T("Next"))
            C.form.add_button("Cancel", cancelar)
            
            if C.form.process().accepted:
                session.q2Wh.estudiante.update(C.form.vars)
                if C.form.vars.con_titulo == 'Sim':
                    session.q2Wh.step = 3
                else:
                    session.q2Wh.step = 4
                redirect(URL('inscribir', args=[C.evento.id]))
            
            return dict(C=C)
        else:
            # -- sino es trabajador seguir al proximo paso
            session.q2Wh.step = 4
            redirect(URL('inscribir', args=[C.evento.id]))
            
    if data.step == 3:
        # -- tipo de titulo que da el trabajo
        C.titulo = T("Información laboral 2/2")
        
        fld_trab_titulo = db.estudiante.get('trab_titulo')
        from agiscore.db.estudiante import TRAB_TITULO_VALUES
        fld_trab_titulo.requires = IS_IN_SET(TRAB_TITULO_VALUES, zero=None)
        
        C.form = SQLFORM.factory(fld_trab_titulo,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        C.form.add_button("Cancel", cancelar)
        
        if C.form.process().accepted:
            session.q2Wh.estudiante.update(C.form.vars)
            session.q2Wh.step = 4
            redirect(URL('inscribir', args=[C.evento.id]))
        
        return dict(C=C)
    
    # Como esto es inscripción la forma de acceso siempre es la misma
    # es decir mediante el examen
    session.q2Wh.estudiante.forma_acceso = '01'
            
    if data.step == 4:
        # -- institucionales
        C.titulo = T("Institucionales")
        
        fld_modalidad = db.estudiante.get("modalidad")
        fld_es_inter = Field('es_inter', 'string', length=3, default='Não')
        fld_es_inter.requires = IS_IN_SET(['Sim', 'Não'], zero=None)
        fld_es_inter.label = T("¿Internato?")
        fld_documentos = db.estudiante.get("documentos")
        fld_discapacidades = db.estudiante.get("discapacidades")
        fld_bolsa_estudio = db.estudiante.get("bolsa_estudio")
        fld_regimen = db.candidatura.get("regimen_id")
        r_set = (db.regimen_unidad_organica.id > 0)
        r_set &= (db.regimen_unidad_organica.unidad_organica_id == C.unidad.id)
        r_set &= (db.regimen_unidad_organica.regimen_id == db.regimen.id) 
        regimenes = []
        for r in db(r_set).select():
            regimenes.append((r.regimen_unidad_organica.id, r.regimen.nombre))
        fld_regimen.requires = IS_IN_SET(regimenes, zero=None)
                
        C.form = SQLFORM.factory(fld_modalidad,
                                 fld_es_inter,
                                 fld_documentos,
                                 fld_discapacidades,
                                 fld_bolsa_estudio,
                                 fld_regimen,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        C.form.add_button("Cancel", cancelar)
        
        if C.form.process().accepted:
            vals = C.form.vars
            vals.es_internado = False if vals.es_inter == 'Não' else True
            # por defecto como es nuevo se pone que viene de examenes de ingreso
            # cuando se realiza la matricula se puede poner otro valor
            from agiscore.db.estudiante import FA_EXAME_DE_INGRESSO
            vals.forma_acceso = FA_EXAME_DE_INGRESSO
            vals.ano_ies = str(date.today().year)
            vals.ano_es = str(date.today().year)
            vals.unidad_organica_id = C.unidad.id
            session.q2Wh.candidatura.regimen_id = db.candidatura.regimen_id.validate(vals.regimen_id)[0]
            session.q2Wh.estudiante.update(vals)
            session.q2Wh.step = 5
            redirect(URL('inscribir', args=[C.evento.id]))
    
    if data.step == 5:
        # -- selección de las carreras
        C.titulo = T("Opciones de carreras")
        fld_carrera1 = Field('carrera1', 'reference carrera_uo')
        fld_carrera1.label = T("Opción 1")
        fld_carrera2 = Field('carrera2', 'reference carrera_uo')
        fld_carrera2.label = T("Opción 2")
        
        # -- carreras posibles
        c_set = (db.carrera_uo.id > 0)
        c_set &= (db.carrera_uo.unidad_organica_id == C.unidad.id)
        c_set &= (db.carrera_uo.carrera_escuela_id == db.carrera_escuela.id)
        c_set &= (db.carrera_escuela.descripcion_id == db.descripcion_carrera.id)
        c_set &= (db.carrera_uo.id == db.plazas.carrera_id)
        c_set &= (db.plazas.ano_academico_id == C.ano.id)
        c_set &= (db.plazas.regimen_id == session.q2Wh.candidatura.regimen_id)
        c_set &= (db.plazas.necesarias > 0)
        posibles = []
        for r in db(c_set).select():
            posibles.append((r.carrera_uo.id,
                             r.descripcion_carrera.nombre))
        fld_carrera1.requires = IS_IN_SET(posibles, zero=None)
        fld_carrera2.requires = IS_IN_SET(posibles, zero=None)
        
        C.form = SQLFORM.factory(fld_carrera1,
                                 fld_carrera2,
                                 table_name="candidatura_carrera",
                                 submit_button=T("Inscribir"))
        C.form.add_button("Cancel", cancelar)
        
        if C.form.process().accepted:
            vals = C.form.vars
            session.q2Wh.c_c_1 = vals.carrera1
            session.q2Wh.c_c_2 = vals.carrera2
            session.q2Wh.step = 6
            redirect(URL('inscribir', args=[C.evento.id]))
        
        return dict(C=C)
    
    if data.step == 6:
        # -- crear los registros
        persona_id = db.persona.insert(**db.persona._filter_fields(session.q2Wh.persona))
        vals = session.q2Wh.estudiante
        vals.persona_id = persona_id
        estudiante_id = db.estudiante.insert(**db.estudiante._filter_fields(vals))
        vals = session.q2Wh.candidatura
        vals.ano_academico_id = C.ano.id
        vals.estudiante_id = estudiante_id
        cand_id = db.candidatura.insert(**db.candidatura._filter_fields(vals))
        vals = session.q2Wh
        db.candidatura_carrera.insert(candidatura_id=cand_id,
                                      carrera_id=vals.c_c_1,
                                      prioridad=1)
        db.candidatura_carrera.insert(candidatura_id=cand_id,
                                      carrera_id=vals.c_c_2,
                                      prioridad=2)
        session.q2Wh = None
        redirect(URL('candidaturas', args=[C.evento.id]))
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def asignar_carreras():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    
    from agiscore.db.asignacion_carrera import asignarCarreras
    # TODO: esto no debe pasar para eventos inactivos
    q = (db.regimen_unidad_organica.id > 0) & \
        (db.regimen_unidad_organica.unidad_organica_id == C.unidad.id)
    for r in db(q).select():
        asignarCarreras(C.evento.id, r.id)
    
    session.flash = T('Asignaciones realizadas')
    redirect(URL('candidaturas', args=[request.args(0)]))
    
    return dict(C=C)

# TODO: chequear más tade si se pueden poner restricciones adicionales
@auth.requires_login()
def candidaturas():
    '''Mostrar el registro de candidatos para el evento de inscripción'''
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Candidaturas"))
    
    # --permisos
    puede_crear = (auth.has_membership(role=myconf.take('roles.admin')) or 
                   auth.has_membership(role=myconf.take('roles.incribidor'))) 
    puede_editar = auth.has_membership(role=myconf.take('roles.admin'))
    puede_borrar = auth.has_membership(role=myconf.take('roles.admin'))
    
    # puede_crear aqui es si el usuario puede inscribir candidatos
    puede_crear &= esta_activo(C.evento)
    
    C.crear = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                         ' ',
                         T("Iniciar candidatura")),
                     URL('inscribir', args=[C.evento.id]),
                     puede_crear,
                     _class="btn btn-default")
    
    C.asignar = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                         ' ',
                         T("Asignar carreras")),
                     URL('asignar_carreras', args=[C.evento.id]),
                     auth.has_membership(role=myconf.take('roles.admin')),
                     _class="btn btn-danger",
                     _title=T("""Es un proceso largo y consume muchos recursos, activar solo cuando sea necesario"""))
    
    # -- preparar el grid
    tbl = db.candidatura
    
    # -- configurar consulta
    query = (tbl.id > 0)
    query &= (tbl.ano_academico_id == C.ano.id)
    query &= (tbl.estudiante_id == db.estudiante.id)
    query &= (db.estudiante.persona_id == db.persona.id)
    
    exportadores = dict(xml=False, html=False, csv_with_hidden_cols=False,
        csv=False, tsv_with_hidden_cols=False, tsv=False, json=False,
        PDF=(tools.ExporterPDF, 'PDF'))
    
    # -- configuración de los campos
    campos = [tbl.id,
              tbl.numero_inscripcion,
              db.estudiante.id,
              db.persona.nombre_completo,
              tbl.regimen_id,
              tbl.estado_candidatura, ]
    for f in tbl:
        f.readable = False
    tbl.numero_inscripcion.readable = True
    tbl.regimen_id.represent = lambda id, r: \
        db.regimen(db.regimen_unidad_organica(id).regimen_id).abreviatura
    tbl.regimen_id.readable = True
    tbl.estado_candidatura.readable = True
    for f in db.estudiante:
        f.readable = False
    for f in db.persona:
        f.readable = False
    db.persona.nombre_completo.readable = True
    tbl.numero_inscripcion.label = T("# Ins.")
    db.persona.nombre_completo.label = T("Nombre")
    
    text_lengths = {'persona.nombre_completo': 45}
    
    # enlaces a las operaciones
    from agiscore.db import candidatura
    def _enlaces(row):
        _cand = db.candidatura(row.candidatura.id)
        co = CAT()
        
        pago_link = URL('pago_inscripcion', args=[C.evento.id,
                                                  _cand.id])
        puede_pagar = auth.has_membership(role=myconf.take('roles.admin'))
        puede_pagar |= auth.has_membership(role=myconf.take('roles.cinscrip'))
        if  _cand.estado_candidatura == candidatura.INSCRITO_CON_DEUDAS:
            puede_pagar &= True
        else:
            puede_pagar &= False
            
        puede_pagar &= esta_activo(C.evento)
        if puede_pagar:
            co.append(Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                                 ' ',
                                 T("Falta de pago")),
                             pago_link,
                             puede_pagar,
                             _class="btn btn-default btn-sm"))
        
        editar_link = URL('editar', args=[C.evento.id,
                                          _cand.id])
        editar_perm = auth.has_membership(role=myconf.take('roles.admin'))            
        editar_perm &= esta_activo(C.evento)
        co.append(Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                             ' ',
                             T("Editar")),
                         editar_link,
                         editar_perm,
                         _class="btn btn-default btn-sm"))
        
        return co
    enlaces = [dict(header='', body=_enlaces)]
    
    if request.vars._export_type:
        response.context = C
    
    C.grid = grid_simple(query,
                         create=False,
                         editable=False,
                         csv=puede_crear,
                         fields=campos,
                         deletable=puede_borrar,
                         maxtextlengths=text_lengths,
                         exportclasses=exportadores,
                         orderby=[db.persona.nombre_completo],
                         links=enlaces,
                         args=request.args[:1])
    
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')) or
               auth.has_membership(role=myconf.take('roles.cinscrip')))
def pago_inscripcion():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    C.candidato = db.candidatura(request.args(1))
    C.estudiante = db.estudiante(C.candidato.estudiante_id)
    C.persona = db.persona(C.estudiante.persona_id)
    if C.candidato is None:
        raise HTTP(404)
    
    # buscar un tipo de pago que coincida en nombre con el tipo de evento
    concepto = db(
        db.tipo_pago.nombre == "INSCRIÇÃO AO EXAME DE ACESSO"
    ).select().first()
    if not concepto:
        raise HTTP(404)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Pago") + " de {}".format(concepto.nombre))
    
    campos = list()
    fld_cantidad = db.pago.get("cantidad")
    fld_cantidad.requires.append(
        IS_FLOAT_IN_RANGE(concepto.cantidad,
                          9999999999.99,
                          error_message=T("Debe ser mayor que {0}".format(concepto.cantidad))))
    campos.append(db.pago.get("forma_pago"))
    campos.append(fld_cantidad)
    campos.append(db.pago.get("numero_transaccion"))
    campos.append(db.pago.get("transaccion"))
    campos.append(db.pago.get("codigo_recivo"))
    campos.append(db.pago.get("fecha_recivo"))
    back = URL('candidaturas', args=[C.evento.id])
    manejo = SQLFORM.factory(*campos, submit_button=T('Inscribir'))
    manejo.add_button(T("Cancel"), back)
    C.form = manejo
    C.titulo = "{} {} - {}".format(T("Pago"),
                         concepto.nombre,
                         C.persona.nombre_completo)
    if manejo.process().accepted:
        valores = manejo.vars
        valores.tipo_pago_id = concepto.id
        valores.persona_id = C.persona.id
        valores.evento_id = C.evento.id
        db.pago.insert(**db.pago._filter_fields(valores))
        db.commit()
        sum_q = db.pago.cantidad.sum()
        q = (db.pago.persona_id == valores.persona_id)
        q &= (db.pago.tipo_pago_id == concepto.id)
        total = db(q).select(sum_q).first()[sum_q]
        if total >= concepto.cantidad:
            from agiscore.db import candidatura, examen
            candidatura.inscribir(C.persona.id, C.evento.id)
            # -- agregado por #70: generar los examenes de inscripción 
            # si al agregar al candidato se registra una asignatura nueva
            generar_examenes_acceso_ex(C.evento, db)
        session.flash = T('Pago registrado')
        redirect(back)
    
    return dict(C=C)

@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def configurar():
    """Configuración del evento"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Ajustes"))
    
    back_url = URL('index', args=[C.evento.id])
    
    C.form = form_configurar_evento(C.evento, back_url,
                                    db=db,
                                    request=request,
                                    T=T)
    if C.form.process().accepted:
        session.flash = T("Ajustes guardados")
        redirect(back_url)

    return dict(C=C)


@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
def editar():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)
    C.candidatura = db.candidatura(request.args(1))
    C.estudiante = db.estudiante(C.candidatura.estudiante_id)
    C.persona = db.persona(C.estudiante.persona_id)
    C.op1 = db.candidatura_carrera(candidatura_id=C.candidatura.id,
                                 prioridad=1)
    C.op2 = db.candidatura_carrera(candidatura_id=C.candidatura.id,
                                 prioridad=2)
    
    if C.persona is None:
        raise HTTP(404)
    
    # breadcumbs
    u_link = Accion(C.unidad.abreviatura or C.unidad.nombre,
                    URL('unidad', 'index', args=[C.unidad.id]),
                    True)  # siempre dentro de esta funcion
    menu_migas.append(u_link)
    a_links = Accion(C.ano.nombre,
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("EDITAR CANDIDATURA"))
    
    # inicializar el proceso
    # -- cancelar
    mi_vars = Storage(request.vars)  # make a copy
    mi_vars._formulario_inscribir = 1
    cancelar = URL(c=request.controller, f=request.function,
                   args=request.args, vars=mi_vars)
    back = URL('candidaturas', args=[C.evento.id])
    proximo = URL(c=request.controller,
               f=request.function,
               args=request.args,
               vars=request.vars)
    
    if request.vars._formulario_inscribir:
        session.sd2fh = None
        redirect(back)
        
    if session.sd2fh is None:
        session.sd2fh = Storage(dict(step=0))
        session.sd2fh.persona = Storage()
        session.sd2fh.estudiante = Storage()
        session.sd2fh.candidatura = Storage()
        session.sd2fh.op1 = Storage()
        session.sd2fh.op2 = Storage()
    data = session.sd2fh
    step = data.step
    
    # ------------------------------------------------- PERSONA
    
    if step == 0:
        # datos personales
        fld_nombre = db.persona.get("nombre")
        fld_apellido1 = db.persona.get("apellido1")
        fld_apellido2 = db.persona.get("apellido2")
        fld_fecha_nacimiento = db.persona.get("fecha_nacimiento")
        fld_genero = db.persona.get("genero")
        fld_padre = db.persona.get("nombre_padre")
        fld_madre = db.persona.get("nombre_madre")
        fld_estado_civil = db.persona.get("estado_civil")
        fld_estado_politico = db.persona.get("estado_politico")
        fld_situacion_militar = db.persona.get("situacion_militar")
        fld_pais_origen = db.persona.get("pais_origen")

        fld_nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_apellido1.requires = IS_UPPER()
        fld_apellido2.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        hoy = datetime.date.today()
        _15anos = datetime.timedelta(days=(15 * 365))
        fld_fecha_nacimiento.requires = [IS_DATE_LT(maximo=hoy - _15anos),
                                         IS_NOT_EMPTY()]
        fld_padre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_madre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_pais_origen.requires = IS_IN_DB(db, "pais.id",
                                            "%(nombre)s",
                                            zero=T("(ESCOGER UNO)"))
        
        form = SQLFORM.factory(fld_nombre,
            fld_apellido1,
            fld_apellido2,
            fld_fecha_nacimiento,
            fld_genero,
            fld_padre, fld_madre,
            fld_estado_civil,
            fld_estado_politico,
            fld_situacion_militar,
            fld_pais_origen,
            record=C.persona,
            showid=False,
            table_name="persona",
            submit_button=T("Next"),
            )
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Datos personales")
        if form.process().accepted:
            session.sd2fh.step = 1
            # en form_crear_persona.valores tenemos los datos validados
            session.sd2fh.persona.update(db.persona._filter_fields(form.vars))
            C.persona.update_record(**session.sd2fh.persona)
            redirect(proximo)
        return dict(C=C)
    
    if step == 1:
        # ORIGEN
        # Si el país de origen es ANGOLA, se puede preguntar por el lugar
        # de nacimiento.
        from agiscore.db import pais as pais_model
        origen = db.pais(C.persona.pais_origen)
        campos = list()
        if origen.codigo == pais_model.ANGOLA:
            s = db(db.comuna.id > 0 and db.municipio.id == db.comuna.municipio_id)
            comunas = [(r.comuna.id, "{0} / {1}".format(r.comuna.nombre, r.municipio.nombre)) \
                for r in s.select(orderby=db.comuna.nombre)]
            fld_lugar_nacimiento = db.persona.get("lugar_nacimiento")
            fld_lugar_nacimiento.requires = IS_IN_SET(comunas, zero=T("(ESCOGER UNO)"))
            # -- arreglo para la representasión de las comunas.
            campos.append(fld_lugar_nacimiento)
        else:
            data.persona.lugar_nacimiento = None
            # no debe tener lugar de nacimiento
            C.persona.update_record(lugar_nacimiento=None)
            fld_tiene_nacionalidad = Field('tiene_nacionalidad',
                                           'boolean',
                                           default=True)
            fld_tiene_nacionalidad.label = T("¿Posee nacionalidad angolana?")
            campos.append(fld_tiene_nacionalidad)
        form = SQLFORM.factory(*campos,
                               table_name="persona",
                               submit_button=T("Next"))
        form.vars.update(C.persona)
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Origen")
        if form.process().accepted:
            session.sd2fh.persona.update(db.persona._filter_fields(form.vars))
            C.persona.update_record(**session.sd2fh.persona)
            session.sd2fh.step = 2
            redirect(proximo)
        return dict(C=C)
    
    if data.persona.lugar_nacimiento or data.persona.tiene_nacionalidad:
        # BILHETE DE IDENTIDADE
        session.sd2fh.persona.tipo_documento_identidad_id = 1
    else:
        # PASAPORTE
        session.sd2fh.persona.tipo_documento_identidad_id = 2
        
    if step == 2:
        # residencia 1
        campos = []
        fld_numero_identidad = db.persona.get("numero_identidad")
        fld_pais_residencia = db.persona.get("pais_residencia")
        fld_pais_residencia.requires = IS_IN_DB(db, "pais.id",
                                                "%(nombre)s",
                                                zero=None)
        if data.persona.tipo_documento_identidad_id == 1:
            fld_pais_residencia.default = 3
            fld_numero_identidad.label = T("Carnet de identidad")
        else:
            fld_pais_residencia.default = C.persona.pais_origen
            fld_numero_identidad.label = T("Número de pasaporte")
        fld_numero_identidad.requires = [IS_NOT_EMPTY(), IS_UPPER(),
            IS_NOT_IN_DB(db, "persona.numero_identidad")]
        campos.append(fld_numero_identidad)
        campos.append(fld_pais_residencia)
        form = SQLFORM.factory(*campos,
                               record=C.persona,
                               showid=False,
                               table_name="persona",
                               submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Residencia 1/2")
        if form.process().accepted:
            session.sd2fh.persona.update(db.persona._filter_fields(form.vars))
            C.persona.update_record(**session.sd2fh.persona)
            session.sd2fh.step = 3
            redirect(proximo)
        return dict(C=C)
    
    if step == 3:
        # residencia 2
        from agiscore.db import pais as pais_model
        
        campos = []
        fld_direccion = db.persona.get("direccion")
        pais_residencia = db.pais(C.persona.pais_residencia)
        if pais_residencia.codigo == pais_model.ANGOLA:
            fld_comuna = db.persona.get("dir_comuna_id")
            fld_comuna.label = T("Localidad")
            s = db((db.comuna.id > 0) & (db.municipio.id == db.comuna.municipio_id))
            comunas = [(r.comuna.id, "{0} / {1}".format(r.comuna.nombre, r.municipio.nombre)) \
                for r in s.select(orderby=db.comuna.nombre)]
            fld_comuna.requires = IS_IN_SET(comunas, zero=T("(ESCOGER UNO)"))
            campos.append(fld_comuna)
        campos.append(fld_direccion)
        form = SQLFORM.factory(*campos,
                               record=C.persona,
                               showid=False,
                               table_name="persona",
                               submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Residencia 2/2")
        if form.process().accepted:
            session.sd2fh.persona.update(db.persona._filter_fields(form.vars))
            C.persona.update_record(**session.sd2fh.persona)
            session.sd2fh.step = 4
            redirect(proximo)
        return dict(C=C)
    
    if step == 4:
        # datos de contacto
        campos = []
        fld_telefono = db.persona.get("telefono")
        fld_telefono2 = db.persona.get("telefono_alternativo")
        fld_email = db.persona.get("email")
        fld_email.requires = IS_EMPTY_OR(IS_EMAIL())
        campos.append(fld_telefono)
        campos.append(fld_telefono2)
        campos.append(fld_email)
        form = SQLFORM.factory(*campos,
                               record=C.persona,
                               showid=False,
                               table_name="persona",
                               submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Contacto")
        if form.process().accepted:
            session.sd2fh.persona.update(db.persona._filter_fields(form.vars))
            C.persona.update_record(**session.sd2fh.persona)
            session.sd2fh.step = 5
            redirect(proximo)
        return dict(C=C)

    # ------------------------------------------------- FIN PERSONA
    
    # ------------------------------------------------- ESTUDIANTE
    if step == 5:
        # -- recoger los datos del estudiante
        fld_habilitacion = db.estudiante.get('pro_habilitacion')
        fld_tipo_escuela = db.estudiante.get('pro_tipo_escuela')
        fld_pro_carrera = db.estudiante.get('pro_carrera')
        fld_pro_carrera.comment = T('''
            Nombre de la carrera que concluyó en la enseñanza previa
        ''')
        fld_pro_ano = db.estudiante.get('pro_ano')
        fld_pro_ano.comment = T('''
            Año en que se gradúo en la enseñanza media
        ''')
        fld_pro_ano.requires = IS_IN_SET(range(1950,
                                               datetime.date.today().year + 1),
                                         zero=None)
        fld_pro_ano.default = datetime.date.today().year - 1
        fld_tipo_escuela.requires = IS_IN_DB(db,
                                             'tipo_escuela_media.id',
                                             "%(nombre)s",
                                             zero=T("(ESCOGER UNO)"))
        
        form = SQLFORM.factory(fld_habilitacion,
                                 fld_tipo_escuela,
                                 fld_pro_carrera,
                                 fld_pro_ano,
                                 record=C.estudiante,
                                 showid=False,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        C.titulo = T("Procedencia 1/2")
        if form.process().accepted:
            session.sd2fh.step = 6
            session.sd2fh.estudiante.update(db.estudiante._filter_fields(form.vars))
            C.estudiante.update_record(**session.sd2fh.estudiante)
            redirect(proximo)
            
        return dict(C=C)
    
    if step == 6:
        # --segunda parte de los datos de procedencia
        C.titulo = T("Procedencia 2/2")
        
        # -- configurar campos
        campos = []
        tipo_escuela_id = C.estudiante.pro_tipo_escuela
        tipo_escuela = db.tipo_escuela_media(tipo_escuela_id)
        if tipo_escuela.uuid != "a57d6b2b-8f0e-4962-a2a6-95f5c82e015d":
            fld_pro_escuela = db.estudiante.get("pro_escuela_id")
            esc_set = (db.escuela_media.id > 0)
            esc_set &= (db.escuela_media.tipo_escuela_media_id == tipo_escuela_id)
            fld_pro_escuela.requires = IS_IN_DB(db(esc_set),
                                                db.escuela_media.id,
                                                '%(nombre)s',
                                                zero=None)
            campos.append(fld_pro_escuela)
#         fld_pro_media = db.estudiante.get("pro_media")
#         campos.append(fld_pro_media)
        fld_es_trab = Field('es_trab', 'string', length=1, default='Não')
        fld_es_trab.label = T('¿Es trabajador?')
        fld_es_trab.requires = IS_IN_SET(['Sim', 'Não'], zero=None)
        campos.append(fld_es_trab)
        
        form = SQLFORM.factory(*campos,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        form.vars.update(C.estudiante)
        form.vars.es_trab = 'Sim' if C.estudiante.es_trabajador else 'Não'
        C.grid = form
        
        if form.process().accepted:
            vals = form.vars
            vals.es_trabajador = False if vals.es_trab == 'Não' else True
            session.sd2fh.step = 7
            session.sd2fh.estudiante.update(db.estudiante._filter_fields(form.vars))
            C.estudiante.update_record(**session.sd2fh.estudiante)
            redirect(proximo)
        return dict(C=C)
    
    if step == 7:
        if C.estudiante.es_trabajador:
            # --pedir los datos del centro de trabajo
            C.titulo = T("Información laboral 1/2")
            fld_trab_profesion = db.estudiante.get('trab_profesion')
            fld_trab_profesion.requires = [IS_NOT_EMPTY(), IS_UPPER()]
            fld_trab_nombre = db.estudiante.get("trab_nombre")
            fld_trab_nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
            fld_trab_provincia = db.estudiante.get("trab_provincia")
            fld_trab_provincia.label = T("Provincia")
            fld_trab_provincia.comment = T('''
                Seleccione la provincia donde se desempeña el trabajo
            ''')
            fld_trab_provincia.requires = IS_IN_DB(db, db.provincia.id,
                                                   "%(nombre)s",
                                                   zero=T("(ESCOGER UNO)"))
            fld_trab_tipo_instituto = db.estudiante.get('trab_tipo_instituto')
            from agiscore.db.estudiante import TRAB_TIPO_INSTITUTO
            fld_trab_tipo_instituto.requires = IS_IN_SET(TRAB_TIPO_INSTITUTO,
                                                         zero=None)
            fld_trab_con_titulo = Field('con_titulo', 'string', length=3,
                                        default='Não')
            fld_trab_con_titulo.label = T("¿Tiene salida con título?")
            fld_trab_con_titulo.requires = IS_IN_SET(['Sim', 'Não'], zero=None)
            
            form = SQLFORM.factory(fld_trab_profesion,
                                     fld_trab_nombre,
                                     fld_trab_tipo_instituto,
                                     fld_trab_con_titulo,
                                     fld_trab_provincia,
                                     table_name="estudiante",
                                     submit_button=T("Next"))
            form.add_button("Cancel", cancelar)
            form.vars.update(C.estudiante)
            form.vars.con_titulo = 'Sim' if C.estudiante.trab_titulo else 'Não'
            C.grid = form
            
            if form.process().accepted:
                session.sd2fh.estudiante.update(db.estudiante._filter_fields(form.vars))
                C.estudiante.update_record(**session.sd2fh.estudiante)
                if form.vars.con_titulo == 'Sim':
                    session.sd2fh.step = 8
                else:
                    session.sd2fh.step = 9
                redirect(proximo)
            
            return dict(C=C)
        else:
            # -- sino es trabajador seguir al proximo paso
            session.sd2fh.step = 9
            redirect(proximo)

    if step == 8:
        # -- tipo de titulo que da el trabajo
        C.titulo = T("Información laboral 2/2")
        
        fld_trab_titulo = db.estudiante.get('trab_titulo')
        from agiscore.db.estudiante import TRAB_TITULO_VALUES
        fld_trab_titulo.requires = IS_IN_SET(TRAB_TITULO_VALUES, zero=None)
        
        form = SQLFORM.factory(fld_trab_titulo,
                               record=C.estudiante,
                               showid=False,
                               table_name="estudiante",
                               submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        
        if form.process().accepted:
            session.sd2fh.step = 9
            session.sd2fh.estudiante.update(db.estudiante._filter_fields(form.vars))
            C.estudiante.update_record(**session.sd2fh.estudiante)
            redirect(proximo)
        
        return dict(C=C)
    
    if step == 9:
        # -- institucionales
        C.titulo = T("Institucionales")
        fld_es_internado = db.estudiante.get("es_internado")
        fld_documentos = db.estudiante.get("documentos")
        fld_discapacidades = db.estudiante.get("discapacidades")
        fld_bolsa_estudio = db.estudiante.get("bolsa_estudio")
                
        form = SQLFORM.factory(fld_es_internado,
                                 fld_documentos,
                                 fld_discapacidades,
                                 fld_bolsa_estudio,
                                 record=C.estudiante,
                                 showid=False,
                                 table_name="estudiante",
                                 submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        C.grid = form
        
        if form.process().accepted:
            session.sd2fh.step = 10
            session.sd2fh.estudiante.update(db.estudiante._filter_fields(form.vars))
            C.estudiante.update_record(**session.sd2fh.estudiante)
            redirect(proximo)
            
        return dict(C=C)
    # ------------------------------------------------- FIN ESTUDIANTE
    
    # ------------------------------------------------- CANDIDATURA
    if step == 10:
        C.titulo = T("Candidatura 1/3")
        
        campos = []
        fld_regimen = db.matricula.get("regimen_id")
        campos.append(fld_regimen)
        
        form = SQLFORM.factory(*campos,
                               showid=False,
                               record=C.candidatura,
                               table_name="candidatura",
                               submit_button=T("Next"))

        form.add_button("Cancel", cancelar)
        C.grid = form
        
        if form.process().accepted:
            session.sd2fh.step = 11
            session.sd2fh.candidatura.update(db.matricula._filter_fields(form.vars))
            C.candidatura.update_record(**session.sd2fh.candidatura)
            redirect(proximo)
            
        return dict(C=C)
    
    if step == 11:
        C.titulo = T("Candidatura 2/3")
                
        campos = []
        fld_op1 = db.candidatura_carrera.get("carrera_id")
        # -- carreras posibles
        c_set = (db.carrera_uo.id > 0)
        c_set &= (db.carrera_uo.unidad_organica_id == C.unidad.id)
        c_set &= (db.carrera_uo.carrera_escuela_id == db.carrera_escuela.id)
        c_set &= (db.carrera_escuela.descripcion_id == db.descripcion_carrera.id)
        c_set &= (db.carrera_uo.id == db.plazas.carrera_id)
        c_set &= (db.plazas.ano_academico_id == C.ano.id)
        c_set &= (db.plazas.regimen_id == session.sd2fh.candidatura.regimen_id)
        c_set &= (db.plazas.necesarias > 0)
        posibles = []
        for r in db(c_set).select():
            posibles.append((r.carrera_uo.id,
                             r.descripcion_carrera.nombre))
        fld_op1.requires = IS_IN_SET(posibles, zero=None)
        fld_op1.label = T("Opción 1")
        campos.append(fld_op1)
        
        form = SQLFORM.factory(*campos,
                               showid=False,
                               record=C.op1,
                               table_name="candidatura_carrera",
                               submit_button=T("Next"))

        form.add_button("Cancel", cancelar)
        C.grid = form
        
        if form.process().accepted:
            session.sd2fh.step = 12
            session.sd2fh.op1.update(db.candidatura_carrera._filter_fields(form.vars))
            C.op1.update_record(**session.sd2fh.op1)
            redirect(proximo)
            
        return dict(C=C)

    if step == 12:
        C.titulo = T("Candidatura 3/3")
                
        campos = []
        fld_op2 = db.candidatura_carrera.get("carrera_id")
        # -- carreras posibles
        c_set = (db.carrera_uo.id > 0)
        c_set &= (db.carrera_uo.unidad_organica_id == C.unidad.id)
        c_set &= (db.carrera_uo.carrera_escuela_id == db.carrera_escuela.id)
        c_set &= (db.carrera_escuela.descripcion_id == db.descripcion_carrera.id)
        c_set &= (db.carrera_uo.id == db.plazas.carrera_id)
        c_set &= (db.plazas.ano_academico_id == C.ano.id)
        c_set &= (db.plazas.regimen_id == session.sd2fh.candidatura.regimen_id)
        c_set &= (db.plazas.necesarias > 0)
        posibles = []
        for r in db(c_set).select():
            posibles.append((r.carrera_uo.id,
                             r.descripcion_carrera.nombre))
        fld_op2.requires = IS_IN_SET(posibles, zero=None)
        fld_op2.label = T("Opción 2")
        campos.append(fld_op2)
        
        form = SQLFORM.factory(*campos,
                               showid=False,
                               record=C.op2,
                               table_name="candidatura_carrera",
                               submit_button=T("Next"))

        form.add_button("Cancel", cancelar)
        C.grid = form
        
        if form.process().accepted:
            session.sd2fh.step = 13
            session.sd2fh.op2.update(db.candidatura_carrera._filter_fields(form.vars))
            C.op2.update_record(**session.sd2fh.op2)
            redirect(proximo)
            
        return dict(C=C)
    
    if step == 13:
        # terminar edición
        session.sd2fh = None
        redirect(back)
    # ------------------------------------------------- FIN CANDIDATURA
    return dict(C=C)
