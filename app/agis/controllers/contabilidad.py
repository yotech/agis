# -*- coding: utf-8 -*-
from datetime import datetime

from applications.agis.modules.db import tipo_pago as tp
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import pago
from applications.agis.modules.db import evento

sidenav.append(
    [T('Tipos de Pagos'), # Titulo del elemento
     URL('tipo_pago'), # url para el enlace
     ['tipo_pago'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Registrar pago de inscripción'), # Titulo del elemento
     URL('registrar_pago_inscripcion'), # url para el enlace
     ['registrar_pago_inscripcion'],] # en funciones estará activo este item
)

def index():
    return dict(message="hello from contabilidad.py")

@auth.requires_membership('administrators')
def registrar_pago_inscripcion():
    def generar_enlace(fila):
        return A(T('Registrar pago'),
                 _href=URL('contabilidad',
                           'registrar_pago_inscripcion',
                           vars=dict(step=2,p_id=fila.id))
                )
    if not 'step' in request.vars:
        redirect( URL( 'registrar_pago_inscripcion',vars=dict(step=1) ) )
    step=request.vars.step
    if step=='1':
        manejo = candidatura.obtener_selector_estado(
            link_generator=[dict(header='',body=generar_enlace)]
        )
    elif step=='2':
        pago.definir_tabla()
        # buscar un evento del tipo inscripción que este activo y la fecha actual esta entre el inicio y el fin
        # de evento, para luego ver si existe un tipo de pago que coincida en nombre con el tipo del evento
        # si eso pasa permitir el pago.
        eventos_activos = evento.eventos_activos(tipo='1') # '1' es tipo inscripción
        e = eventos_activos.first()
        if e:
            # buscar un tipo de pago que coincida en nombre con el tipo de evento
            tipo_pago = db( db.tipo_pago.nombre == evento.evento_tipo_represent('1',None)).select().first()
            if not tipo_pago:
                session.flash=T("No se puede realizar el pago porque no hay un evento activo")
                redirect( URL( 'registrar_pago_inscripcion',vars=dict(step=1) ) )
            db.pago.tipo_pago_id.default=tipo_pago.id
            db.pago.tipo_pago_id.writable=False
            db.pago.cantidad.default=tipo_pago.cantidad
            db.pago.cantidad.writable=False
        else:
            session.flash=T("No se puede realizar el pago porque no hay un evento activo")
            redirect( URL( 'registrar_pago_inscripcion',vars=dict(step=1) ) )
        # ------------------------------------------------------------------------------------------------------
        p_id = int(request.vars.p_id)
        db.pago.persona_id.default=p_id
        db.pago.persona_id.writable=False
        manejo = SQLFORM(db.pago, formstyle='bootstrap', submit_button=T( 'Guardar' ))
        if manejo.process().accepted:
            candidatura.cambiar_estado('2', p_id)
            session.flash=T( 'Pago registrado' )
            redirect( URL( 'registrar_pago_inscripcion',vars=dict(step=1) ) )
    return dict( sidenav=sidenav,manejo=manejo,step=step )

@auth.requires_membership('administrators')
def tipo_pago():
    manejo = tp.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )
