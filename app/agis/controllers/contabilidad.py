# -*- coding: utf-8 -*-

if False:
    from gluon import *
    from db import *
    from menu import *
    from menu import menu_lateral, menu_migas
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


# from datetime import datetime
from gluon.storage import Storage
from agiscore import tools
from agiscore.db import tipo_pago as tp
from agiscore.db import candidatura
# from agiscore.db import pago
from agiscore.db import evento
from agiscore.db import examen
from agiscore.db import unidad_organica
from agiscore.db import ano_academico
from agiscore.db import persona
from agiscore.db import estudiante
# from agiscore.db import examen_aula_estudiante
# from agiscore.gui.evento import seleccionar_evento
# from agiscore.gui.candidatura import seleccionar_candidato
from agiscore.gui.ano_academico import seleccionar_ano
# from agiscore.gui.persona import leyenda_persona
# from agiscore.gui.candidatura import leyenda_candidatura
from agiscore.gui.mic import *

rol_admin = auth.has_membership(myconf.take('roles.admin'))

menu_lateral.append(
    Accion(T('Tipos de Pagos'), URL('tipo_pago'), rol_admin),
    ['tipo_pago'])
# menu_lateral.append(
#     Accion(T('Registro de pagos (INSCRIPCIÓN)'),
#            URL('registro_pagos_inscripcion'),
#            rol_admin),
#     ['registro_pagos_inscripcion', 'registrar_pago_inscripcion'])
menu_lateral.append(
    Accion(T('Registro de pagos (INSCRIPCIÓN)'),
           URL('registrar_pago_inscripcion'),
           rol_admin),
    ['registrar_pago_inscripcion'])
menu_migas.append(
    Accion(T('Contabilidad'), URL('index'), rol_admin))

def index():
    redirect(URL('tipo_pago'))
    return dict(message="hello from contabilidad.py")

# @auth.requires(rol_admin)
# def registro_pagos_inscripcion():
#     context = Storage()
#     
#     # seleccionar unidad_organica
#     if not request.vars.unidad_organica_id:
#         return unidad_organica.seleccionar(context)
#     else:
#         context.unidad_organica = db.unidad_organica(
#             int(request.vars.unidad_organica_id))
#         
#     # seleccionar año académico
#     if not request.vars.ano_academico_id:
#         context.manejo = seleccionar_ano(
#             unidad_organica_id=context.unidad_organica.id)
#         return context
#     else:
#         context.ano_academico = db.ano_academico(
#             int(request.vars.ano_academico_id))
#     
#     # buscar el evento de inscripción para el año academico seleccionado
#     ev = db.evento(tipo=evento.INSCRIPCION,
#                    ano_academico_id=context.ano_academico.id)
#     if not ev:
#         raise HTTP(503)  # error esto nunca debe pasar
# 
#     query = (db.pago.id > 0)
#     query &= (db.pago.persona_id == db.estudiante.persona_id)
#     query &= (db.candidatura.estudiante_id == db.estudiante.id)
#     query &= (db.candidatura.ano_academico_id == context.ano_academico.id)
#     query &= (db.persona.id == db.pago.persona_id)
# 
#     manejo = tools.manejo_simple(query,
#                                  crear=False,
#                                  campos=[db.pago.id,
#                                          db.persona.nombre_completo,
#                                          db.candidatura.estado_candidatura,
#                                          db.pago.cantidad])
#     
#     context.manejo = manejo
#     return context

@auth.requires(rol_admin)
def registrar_pago_inscripcion():
    unidad_organica.definir_tabla()
    ano_academico.definir_tabla()
    evento.definir_tabla()
    persona.definir_tabla()
    estudiante.definir_tabla()

    # buscar un tipo de pago que coincida en nombre con el tipo de evento
    concepto = db(
        db.tipo_pago.nombre == "INSCRIÇÃO AO EXAME DE ACESSO"
    ).select().first()
    if not concepto:
        raise HTTP(404)
 
    context = Storage(dict())
    context.mensaje = ''

    menu_migas.append(T('Registro de pagos (INSCRIPCIÓN)'))
    # seleccionar unidad_organica
    if not request.vars.unidad_organica_id:
        return unidad_organica.seleccionar(context)
    else:
        context.unidad_organica = db.unidad_organica(
            int(request.vars.unidad_organica_id))

    if not request.vars.ano_academico_id:
        context.manejo = seleccionar_ano(unidad_organica_id=context.unidad_organica_id)
        return context
    else:
        context.ano_academico = db.ano_academico(int(
            request.vars.ano_academico_id))

    # seleccionar el evento   
    context.evento = db.evento(ano_academico_id=context.ano_academico.id,
                   tipo=evento.INSCRIPCION)
    if context.evento is None:
        # esto no debe pasar
        raise HTTP(503)
     
    if 'new' in request.args:
        print "AGREGANDO"
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
        back = URL('registrar_pago_inscripcion',
                   vars={'unidad_organica_id': request.vars.unidad_organica_id,
                         'ano_academico_id': request.vars.ano_academico_id})
        manejo = SQLFORM.factory(*campos, submit_button=T('Guardar'))
        manejo.add_button(T("Cancelar"), back)
        if manejo.process().accepted:
            valores = manejo.vars
            valores.tipo_pago_id = concepto.id
            valores.persona_id = int(request.vars.persona_id)
            db.pago.insert(**db.pago._filter_fields(valores))
            db.commit()
            sum = db.pago.cantidad.sum()
            q = (db.pago.persona_id == valores.persona_id)
            q &= (db.pago.tipo_pago_id == concepto.id)
            total = db(q).select(sum).first()[sum]
            if total >= concepto.cantidad:
                candidatura.inscribir(valores.persona_id, context.evento.id)
                # -- agregado por #70: generar los examenes de inscripción 
                # para el candidato
                est = db.estudiante(persona_id=valores.persona_id)
                cand = db.candidatura(estudiante_id=est.id)
                examenes_ids = examen.generar_examenes_acceso(
                    cand
                    )
            session.flash = T('Pago registrado')
            redirect(back)
        context.manejo = manejo
        return context

    def _agregar_pago(row):
        """Si el estudiante tienes deudadas crear el enlace para el formulario"""
        cand = db.candidatura(row.candidatura.id)
        con_deuda = (cand.estado_candidatura == candidatura.INSCRITO_CON_DEUDAS)
        link = Accion('',
                   URL('registrar_pago_inscripcion',
                       vars={'unidad_organica_id': cand.unidad_organica_id,
                             'ano_academico_id': cand.ano_academico_id,
                             'persona_id': row.persona.id, },
                       args=['new']
                       ),
                   (rol_admin and con_deuda),
                   SPAN('', _class='glyphicon glyphicon-usd'),
                   _class="btn btn-default",
                   _title=T("Registrar pago inscripción")
                   )
        return link
    
    def _cantidad_avonada(row):
        """calcula la cantidad avonada por la persona según el concepto"""
        sum = db.pago.cantidad.sum()
        query = (db.pago.persona_id == row.persona.id)
        query &= (db.pago.tipo_pago_id == concepto.id)
        total = db(query).select(sum).first()[sum]
        if total is None:
            total = 0.0
        
        return "{0:.2f}".format(total)
    query = (db.persona.id > 0)
    query &= (db.persona.id == db.estudiante.persona_id)
    query &= (db.estudiante.id == db.candidatura.id)
    query &= (db.candidatura.ano_academico_id == context.ano_academico.id)
    query &= (db.candidatura.unidad_organica_id == context.unidad_organica.id)
    enlaces = [dict(header=T("Cantidad Avonada"), body=_cantidad_avonada),
               dict(header="", body=_agregar_pago)]
    # configurar los campos
    db.persona.id.readable = False
    db.estudiante.id.readable = False
    db.estudiante.persona_id.readable = False
    db.candidatura.id.readable = False
    db.candidatura.estudiante_id.readable = False 
    # -------------------------------------------------------------------------
    campos = [db.persona.id,
              db.persona.numero_identidad,
              db.persona.nombre_completo,
              db.candidatura.id,
              db.candidatura.estado_candidatura]
    db.candidatura.id.readable = False
    manejo = tools.manejo_simple(query, enlaces=enlaces,
                         campos=campos, crear=False,
                         borrar=False, editable=False,
                         buscar=True,)
    co = CAT()
    header = DIV(T("Registro de pagos (INSCRIPCIÓN)"), _class="panel-heading")
    body = DIV(manejo, _class="panel-body")
    co.append(DIV(header, body, _class="panel panel-default"))
    context.manejo = co
    return context

@auth.requires(rol_admin)
def tipo_pago():
    menu_migas.append(T('Tipos de pagos'))
    manejo = tp.obtener_manejo()
    return dict(manejo=manejo)
