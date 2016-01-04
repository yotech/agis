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

from gluon.storage import Storage
from agiscore.gui.mic import Accion, grid_simple
# from agiscore.db.evento import evento_tipo_represent
from agiscore.gui.persona import form_crear_persona_ex
from agiscore.db.evento import esta_activo
from agiscore.validators import IS_DATE_GT
from agiscore import tools
from datetime import date

# TODO: remove
response.menu = []

menu_lateral.append(Accion(T('Registro de candidatos'),
                           URL('candidaturas', args=[request.args(0)]),
                           True),
                    ['candidaturas', 'inscribir', 'pago_inscripcion'])
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
    a_links = Accion(T('Años académicos'),
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
        r_q  = (db.regimen_unidad_organica.id > 0) 
        r_q &= (db.regimen_unidad_organica.unidad_organica_id == C.unidad.id)
        
        c_q  = (db.carrera_uo.id > 0)
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
    
    text_lengths = {'plazas.carrera_id': 50,}
    
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
    a_links = Accion(T('Años académicos'),
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
    
    query  = (tbl.id > 0) & (tbl.evento_id == C.evento.id)
    
    tbl.id.readable = False
    tbl.evento_id.default = C.evento.id
    tbl.evento_id.readable = False
    tbl.evento_id.writable = False
    
    if 'new' in request.args:
        a_set  = (db.asignatura.id > 0) 
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
    a_links = Accion(T('Años académicos'),
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
        # obtener todas las candidaturas involucradas en el evento.
        query  = (db.candidatura.id > 0)
        query &= (db.candidatura.ano_academico_id == C.ano.id)
        c_set = db(query).select(db.candidatura.ALL)
        # generar los examenes de acceso
        from agiscore.db.examen import generar_examenes_acceso
        for c in c_set:
            generar_examenes_acceso(c, evento_id=C.evento.id, db=db)
    
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
        redirect(URL('examen','index', args=[request.args(3)]))
    
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
@auth.requires(auth.has_membership(role=myconf.take('roles.admin')))
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
    a_links = Accion(T('Años académicos'),
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
    a_links = Accion(T('Años académicos'),
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Candidaturas"))
    
    # --permisos
    puede_crear = auth.has_membership(role=myconf.take('roles.admin')) 
    puede_editar, puede_borrar = (puede_crear, puede_crear)
    
    # puede_crear aqui es si el usuario puede inscribir candidatos
    puede_crear &= esta_activo(C.evento)
    
    C.crear = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                         ' ',
                         T("Iniciar candidatura")),
                     URL('inscribir', args=[C.evento.id]),
                     puede_crear,
                     _class="btn btn-default")
    
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
              db.persona.nombre_completo,
              tbl.estado_candidatura, ]
    tbl.id.readable = False
    tbl.estudiante_id.readable = False
    db.estudiante.id.readable = False
    db.estudiante.persona_id.readable = False
    db.persona.id.readable = False
    db.persona.nombre_completo.label = T("Nombre")
    tbl.numero_inscripcion.label = T("# Ins.")
    
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
        co.append(Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                             ' ',
                             T("Inscribir")),
                         pago_link,
                         puede_pagar,
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
    
    campos = list()
    fld_cantidad = db.pago.get("cantidad")
    fld_cantidad.requires.append(
        IS_FLOAT_IN_RANGE(concepto.cantidad,
                          9999999999.99,
                          error_message=T("Debe ser mayor que {0}".format(concepto.cantidad))))
    campos.append(db.pago.get("forma_pago"))
    campos.append(fld_cantidad)
    campos.append(db.pago.get("numero_transaccion"))
    campos.append(db.pago.get("codigo_recivo"))
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
            # para el candidato
            examen.generar_examenes_acceso(C.candidato)
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
    a_links = Accion(T('Años académicos'),
                     URL('unidad', 'index', args=[C.unidad.id]),
                     True)
    menu_migas.append(a_links)
    e_link = Accion(C.evento.nombre,
                    URL('index', args=[C.evento.id]),
                    True)
    menu_migas.append(e_link)
    menu_migas.append(T("Ajustes"))
    
    # configurar campos
    tbl = db.evento
    tbl.id.readable = False
    tbl.nombre.writable = False
    tbl.nombre.readable = False
    tbl.tipo.readable = False
    tbl.tipo.writable = False
    tbl.ano_academico_id.writable = False
    tbl.ano_academico_id.readable = False
    
    if request.vars.fecha_inicio:
        # validar que la fecha de inicio este antes que la de fin
        (fecha_inicio, msg) = db.evento.fecha_inicio.validate(
            request.vars.fecha_inicio)
        if msg is None:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(),
                                            IS_DATE_GT(minimum=fecha_inicio)]
        else:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(), IS_DATE()]
    
    C.form = SQLFORM(db.evento, record=C.evento, submit_button=T("Guardar"))
    C.form.add_button(T("Cancelar"), URL('index', args=[C.evento.id]))
    
    if C.form.process().accepted:
        session.flash = T("Ajustes guardados")
        redirect(URL('index', args=[C.evento.id]))

    return dict(C=C)
