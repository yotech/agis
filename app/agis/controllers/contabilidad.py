# -*- coding: utf-8 -*-
from datetime import datetime
from gluon.storage import Storage
from applications.agis.modules.db import tipo_pago as tp
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import pago
from applications.agis.modules.db import evento
from applications.agis.modules.db import examen
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import persona
from applications.agis.modules.db import estudiante
from applications.agis.modules.db import examen_aula_estudiante
from applications.agis.modules.gui import evento as evento_gui
from applications.agis.modules.gui.candidatura import seleccionar_candidato

rol_admin = auth.has_membership(myconf.take('roles.admin'))

menu_lateral.append(
    Accion('Tipos de Pagos', URL('tipo_pago'), rol_admin),
    ['tipo_pago'])
menu_lateral.append(
    Accion('Registrar pago de inscripción',
           URL('registrar_pago_inscripcion'),
           rol_admin),
    ['registrar_pago_inscripcion'])

menu_migas.append(
    Accion('Contabilidad', URL('index'), rol_admin))

def index():
    redirect(URL('tipo_pago'))
    return dict(message="hello from contabilidad.py")

@auth.requires(rol_admin)
def registrar_pago_inscripcion():
    unidad_organica.definir_tabla()
    ano_academico.definir_tabla()
    evento.definir_tabla()
    persona.definir_tabla()
    estudiante.definir_tabla()

    # buscar un tipo de pago que coincida en nombre con el tipo de evento
    tipo_pago = db(
        db.tipo_pago.nombre == evento.EVENTO_TIPO_VALUES['1']
    ).select().first()
    if not tipo_pago:
        session.flash=T("Defina un tipo de pago para {0}".format(
            evento.EVENTO_TIPO_VALUES['1']))
        redirect( URL( 'tipo_pago') )

    context = Storage(dict())
    context.mensaje = ''

    menu_migas.append(T('Registrar pago de inscripción'))
    # seleccionar unidad_organica
    if not request.vars.unidad_organica_id:
        return unidad_organica.seleccionar(context)
    else:
        context.unidad_organica = db.unidad_organica(
            int(request.vars.unidad_organica_id))

    # seleccionar el evento
    if not request.vars.evento_id:
        context.mensaje = T("Seleccione el evento inscripción")
        return evento_gui.seleccionar(context)
    else:
        context.evento =  db.evento(int(request.vars.evento_id))

    # seleccionar candidato
    if not request.vars.candidatura_id:
        context.mensaje = T("Seleccione persona a realizar el pago")
        db.persona.nombre_completo.label = T('Nombre')
        db.candidatura.id.readable = False
        context.manejo = seleccionar_candidato(estado_candidatura='1',
            unidad_organica_id=context.unidad_organica_id,
            ano_academico_id=context.evento.ano_academico_id)
        return context
    else:
        c = db.candidatura(int(request.vars.candidatura_id))
        e = db.estudiante(c.estudiante_id)
        context.candidatura = c
        context.persona = db.persona(e.persona_id)

    db.pago.tipo_pago_id.default=tipo_pago.id
    db.pago.tipo_pago_id.writable=False
    db.pago.cantidad.default=tipo_pago.cantidad
    db.pago.cantidad.writable=False
    db.pago.persona_id.default = context.persona.id
    db.pago.persona_id.writable = False
    manejo = SQLFORM(db.pago, submit_button=T( 'Guardar' ))
    if manejo.process().accepted:
        candidatura.inscribir(context.persona.id, context.evento.id)
        # -- agregado por #70: generar los examenes de inscripción para el candidato
        examenes_ids = examen.generar_examenes_acceso(
            context.candidatura
            )
        # -- redistribuir las aulas para el examen
        # -- TODO: quitar si se pone lento
#         for id in examenes_ids:
#             examen_aula_estudiante.distribuir_estudiantes(id)
        # -----------------------------------------------------------
        session.flash=T( 'Pago registrado' )
        redirect(URL('registrar_pago_inscripcion',
                     vars=dict(unidad_organica_id=context.unidad_organica.id,
                               evento_id=context.evento.id)
                     ))
    context.manejo = manejo
    return context

@auth.requires(rol_admin)
def tipo_pago():
    menu_migas.append(T('Tipos de pagos'))
    manejo = tp.obtener_manejo()
    return dict( manejo=manejo )
