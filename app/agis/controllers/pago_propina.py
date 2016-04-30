# -*- coding: utf-8 -*-
from datetime import date
from gluon import *
from gluon.storage import Storage
from agiscore.gui.mic import grid_simple
from agiscore.db.pago_propina import pagar_propinas


@auth.requires_signature()
def index():
    """Carga la UI para la realización de los pagos"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))

    return dict(C=C)

@auth.requires_signature()
def formulario():
    """Muestra formulario para realizar pago"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    concepto = db(
        db.tipo_pago.nombre == "PROPINA"
    ).select().first()

    C.titulo = T("Agregar pago")

    fld_forma_pago = db.pago.forma_pago
    fld_numero_transaccion = db.pago.numero_transaccion
    fld_transaccion = db.pago.transaccion
    fld_cantidad = db.pago.cantidad
    fld_codigo_recivo = db.pago.codigo_recivo
    fld_fecha_recivo = db.pago.fecha_recivo

    form = SQLFORM.factory(
        # campos...
        fld_forma_pago,
        fld_numero_transaccion,
        fld_transaccion,
        fld_codigo_recivo,
        fld_fecha_recivo,
        fld_cantidad,
        formstyle="bootstrap3_stacked"
    )

    if form.process().accepted:
        data = form.vars
        data.tipo_pago_id = concepto.id
        data.persona_id = C.persona.id
        data.evento_id = C.evento.id
        pago_id = db.pago.insert(**db.pago._filter_fields(data))
        # Intentar pagar las propinas que se deben
        pagar_propinas(C.evento.id, C.persona.id, db)
        response.js = "jQuery('#formulario_cmp').get(0).reload();jQuery('#pagos_cmp').get(0).reload();jQuery('#propinas_cmp').get(0).reload()"
        return T("Procesando...")

    C.form = form
    return dict(C=C)

@auth.requires_signature()
def propinas():
    """Muestra el listado de los pagos realizados"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    concepto = db(
        db.tipo_pago.nombre == "PROPINA"
    ).select().first()
    assert concepto != None

    C.titulo = T("Registro de Propinas")

    query  = (db.propina.id > 0)
    query &= (db.propina.persona_id == C.persona.id)
    query &= (db.propina.ano_academico_id == C.ano.id)

    # configurar campos
    db.propina.id.readable = False
    # db.propina.pago_id.readable = True

    C.grid = grid_simple(query,
        create=False,
        history=False,
        details=False,
        searchable=False,
        paginate=13,
        csv=False,
        args=request.args[:2],
        formname="propinas"
    )

    return dict(C=C)

@auth.requires_signature()
def pagos():
    """Muestra el listado de los pagos realizados"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    concepto = db(
        db.tipo_pago.nombre == "PROPINA"
    ).select().first()
    assert concepto != None

    query  = (db.pago.id > 0)
    query &= (db.pago.persona_id == C.persona.id)
    query &= (db.pago.evento_id == C.evento.id)
    query &= (db.pago.tipo_pago_id == concepto.id)
    l_pagos = [p.id for p in db(query).select(db.pago.id)]
    sumq = db.pago.cantidad.sum()
    C.total = db(query).select(sumq).first()[sumq] or 0.0
    sumz = db.propina.cantidad.sum()
    pquery  = (db.propina.id > 0)
    pquery &= (db.propina.persona_id == C.persona.id)
    pquery &= (db.propina.ano_academico_id == C.ano.id)
    C.propinas = db(pquery).select(sumz).first()[sumz] or 0.0

    for f in db.pago:
        f.readable = False
    db.pago.id.readable = True
    db.pago.fecha_recivo.readable = True
    db.pago.cantidad.readable = True

    db.pago.id.represent = lambda v,r: A(
        v, _href=URL(c='gcontable',
            f='pagos',
            args=['view', 'pago', v],
            extension=False,
            user_signature=True)
        )

    db.pago.id.label = T("ID Pago")

    C.titulo = T("Registro de pagos")
    C.titulo += " {}".format(C.persona.nombre_completo)
    C.grid = grid_simple(query,
        orderby=[db.pago.fecha_recivo],
        # fields=campos,
        create=False,
        history=False,
        details=False,
        csv=False,
        args=request.args[:2],
        formname="pagos")

    return dict(C=C)
