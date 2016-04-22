# -*- coding: utf-8 -*-
from datetime import date
from gluon import *
from gluon.storage import Storage
from agiscore.gui.mic import grid_simple


@auth.requires_signature()
def index():
    """Carga la UI para la realización de los pagos"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))

    return dict(C=C)

@auth.requires_signature()
def cancelar():
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))

    response.js = "jQuery('#formulario_cmp').get(0).reload();jQuery('#listado_cmp').get(0).reload()"
    session.FP01 = None

    return T("Procesando..")

@auth.requires_signature()
def formulario():
    """Muestra formulario para realizar pago"""
    C = Storage()
    C.evento = db.evento(request.args(0))
    C.persona = db.persona(request.args(1))
    C.ano = db.ano_academico(C.evento.ano_academico_id)
    C.unidad = db.unidad_organica(C.ano.unidad_organica_id)
    C.escuela = db.escuela(C.unidad.escuela_id)

    C.back = URL("cancelar",
        args=[C.evento.id, C.persona.id],
        user_signature=True)

    if session.FP01 is None:
        session.FP01 = Storage()
        session.persona_id = C.persona.id
        session.evento_id = C.evento.id
        session.FP01.step = 0
    else:
        if (session.persona_id != C.persona.id) or (session.evento_id != C.evento.id):
            session.FP01 = None
            response.js = "jQuery('#formulario_cmp').get(0).reload();jQuery('#listado_cmp').get(0).reload()"
            return T("Procesando...")
    step = session.FP01.step
    C.step = step
    C.titulo = T("Agregar pago")

    if step == 0:
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
            session.FP01.update(form.vars)
            session.FP01.step += 1
            # response.js = 'web2py_component("{}","{}");'.format(url, request.cid)
            response.js = "jQuery('#formulario_cmp').get(0).reload()"
            response.flash = None
            return T("Procesando...")

        C.form = form
        return dict(C=C)

    if step == 1:
        # buscar los meses que se han pagado y analizar los meses por pagar
        concepto = db(
            db.tipo_pago.nombre == "PROPINA"
        ).select().first()
        assert concepto != None

        query  = (db.propina.pago_id == db.pago.id)
        query &= (db.pago.persona_id == C.persona.id)
        query &= (db.pago.evento_id == C.evento.id)
        query &= (db.pago.tipo_pago_id == concepto.id)
        rows = db(query).select(db.propina.mes,
            orderby=db.propina.mes,
            distinct=True)
        pagados = [row.mes for row in rows]
        saldo = session.FP01.cantidad
        meses_a_pagar = list(set(C.ano.meses) - set(pagados))
        # si ya no hay meses a pagar para el año.
        if not meses_a_pagar:
            session.FP01 = None
            response.js = "jQuery('#formulario_cmp').get(0).reload()"
            response.flash = T("Ya se han pagado todas las propinas del año académico")
            return T("Procesando...")
        # meses que se pueden pagar con cantidad
        meses_posibles = []
        hoy = date.today()
        while saldo >= concepto.cantidad and meses_a_pagar:
            mes = meses_a_pagar[0]
            if mes < (hoy.month - 1):
                #aplicar multa
                descontar = (concepto.cantidad + (concepto.cantidad * C.ano.multa)/100)
            elif mes == (hoy.month - 1):
                # ver por el día
                if hoy.day > C.ano.dia_limite:
                    descontar = (concepto.cantidad + (concepto.cantidad * C.ano.multa)/100)
                else:
                    descontar = concepto.cantidad
            else:
                descontar = concepto.cantidad
            saldo = saldo - descontar

            meses_a_pagar = list(set(meses_a_pagar) - set([mes]))
            meses_posibles.append((mes, descontar))
        C.meses = meses_posibles
        C.dona = saldo
        session.FP01.meses_posibles = meses_posibles

        form = FORM.confirm('¿Proceder con el pago?')
        if form.accepted:
            # recargar componentes
            data = session.FP01
            data.tipo_pago_id = concepto.id
            data.persona_id = C.persona.id
            data.evento_id = C.evento.id
            pago_id = db.pago.insert(**db.pago._filter_fields(data))
            for m, c in data.meses_posibles:
                db.propina.insert(pago_id=pago_id, mes=m)
            response.js = "jQuery('#formulario_cmp').get(0).reload();jQuery('#listado_cmp').get(0).reload()"
            session.FP01 = None
            return T("Procesando...")

        C.form = form
        return dict(C=C)

    return dict(C=C)

@auth.requires_signature()
def listado():
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

    query  = (db.propina.pago_id == db.pago.id)
    query &= (db.pago.persona_id == C.persona.id)
    query &= (db.pago.evento_id == C.evento.id)
    query &= (db.pago.tipo_pago_id == concepto.id)

    for f in db.propina:
        f.readable = False
    for f in db.pago:
        f.readable = False
    db.pago.id.readable = True
    db.pago.fecha_recivo.readable = True
    db.propina.mes.readable = True

    #configuracion de los campos
    campos = [db.propina.mes,
        db.pago.cantidad,
        db.pago.fecha_recivo,
        db.pago.id]
    db.pago.id.label = T("ID Pago")

    C.titulo = T("Registro de pagos propina")
    C.titulo += " {}".format(C.persona.nombre_completo)
    C.grid = grid_simple(query,
        orderby=[db.propina.mes],
        fields=campos,
        create=False,
        history=False,
        details=False,
        csv=False,
        args=request.args[:2],
        formname="propina_listado")

    return dict(C=C)
