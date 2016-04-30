# -*- coding: utf-8 -*-
import calendar
from datetime import date
from gluon import *

from agiscore.db import persona
from agiscore.db import tipo_pago
from agiscore.db import pago


def mes_represent(valor, fila):
    T = current.T
    return T(calendar.month_name[valor])

def cantidad_represent(valor, fila):
    import locale
    T = current.T

    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    if valor is None:
        return 'N/A'
    return locale.currency(valor, grouping=True)

def pagar_propinas(evento_id, persona_id, db):
    """Intenta realizar pago de propina para los meses que debe el estudiante"""
    evento = db.evento(evento_id)
    persona = db.persona(persona_id)
    ano = db.ano_academico(evento.ano_academico_id)

    concepto = db(
        db.tipo_pago.nombre == "PROPINA"
    ).select().first()

    query  = (db.pago.id > 0)
    query &= (db.pago.persona_id == persona.id)
    query &= (db.pago.evento_id == evento.id)
    query &= (db.pago.tipo_pago_id == concepto.id)
    sumq = db.pago.cantidad.sum()
    l_pagos = [p.id for p in db(query).select(db.pago.id)]

    # limpiar las propinas de esta persona
    db(
        (db.propina.persona_id == persona.id) &
        (db.propina.ano_academico_id == ano.id)
    ).delete()
    db.commit()

    # meses a pagar
    meses_a_pagar = ano.meses
    meses_a_pagar.sort()
    # print meses_a_pagar
    consumido = 0.0
    usados = []
    multa = 0
    for mes in meses_a_pagar:
        # print "Analizando mes: ", mes
        f_limite = date(int(ano.nombre), mes + 1, ano.dia_limite)
        # pagos disponibles
        query  = (db.pago.id > 0)
        query &= (db.pago.persona_id == persona.id)
        query &= (db.pago.evento_id == evento.id)
        query &= (db.pago.tipo_pago_id == concepto.id)
        query &= (db.pago.fecha_recivo < f_limite)

        # saldo disponible para el mes
        saldo_mes = db(query).select(sumq).first()[sumq] or 0.0
        saldo_mes = saldo_mes - consumido
        if saldo_mes >= concepto.cantidad:
            multa = 0
            l_pagos = [p.id for p in db(query).select(db.pago.id)]
            l_pagos.sort()
            # se puede hacer el pago de propina con estos pagos
            db.propina.insert(
                pago_id=l_pagos,
                mes=mes,
                cantidad=concepto.cantidad,
                multa=multa,
                persona_id=persona.id,
                ano_academico_id=ano.id
            )
            usados.extend(l_pagos)
            consumido += concepto.cantidad
        else:
            # hay que tener encuenta todos los pagos y aplicar la multa.
            query  = (db.pago.id > 0)
            query &= (db.pago.persona_id == persona.id)
            query &= (db.pago.evento_id == evento.id)
            query &= (db.pago.tipo_pago_id == concepto.id)
            saldo_mes = db(query).select(sumq).first()[sumq] or 0.0
            saldo_mes = saldo_mes - consumido
            multa = (concepto.cantidad * ano.multa) / 100
            if saldo_mes >= (concepto.cantidad + multa):
                # se hace el pago con multa
                l_pagos = [p.id for p in db(query).select(db.pago.id)]
                l_pagos.sort()
                db.propina.insert(
                    pago_id=l_pagos,
                    mes=mes,
                    cantidad=concepto.cantidad + multa,
                    multa=multa,
                    persona_id=persona.id,
                    ano_academico_id=ano.id
                )
                usados.extend(l_pagos)
                consumido += (concepto.cantidad + multa)
            else:
                break
    # if multa > 0:
        # si multa > 0 entonces es que hay deudas
        # pros = db(
        #     (db.propina.persona_id == persona.id) &
        #     (db.propina.ano_academico_id == ano.id)
        # ).select()
        # meses_pagos = [p.mes for p in pros]
        # meses_pagos.sort()
        # a_pagar = list(set(ano.meses) - set(meses_pagos))
        # a_pagar.sort() # a_pagar[1] es el proximo mes cuando se aplica multa
        # f_limite = date(int(ano.nombre), date.today().month() + 1, ano.dia_limite)
        # from agiscore.db.matricula import MATRICULADO_CON_DEUDAS
        # est = db.estudiante(persona_id=persona.id)
        # mat = db.matricula(estudiante_id=est.id, ano_academico_id=ano.id)
        # mat.update_record(estado_uo=MATRICULADO_CON_DEUDAS)
    db.commit()

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T

    pago.definir_tabla(db, T)
    if not hasattr(db, 'propina'):
        tbl = db.define_table('propina',
            Field('pago_id', 'list:reference pago'),
            Field('mes', 'integer'),
            Field('cantidad', 'float'),
            Field('multa', 'float'),
            Field('persona_id', 'reference persona'),
            Field('ano_academico_id', 'reference ano_academico')
        )
        tbl.persona_id.readable = False
        tbl.ano_academico_id.readable = False
        tbl.mes.label = T("Mes")
        tbl.pago_id.label = T("Info. Pago")
        tbl.cantidad.label = T("Cantidad")
        tbl.multa.label = "**"
        tbl.pago_id.readable = False
        tbl.mes.requires = IS_INT_IN_RANGE(1, 13)
        tbl.mes.represent = mes_represent
        tbl.cantidad.represent = cantidad_represent
        tbl.multa.represent = cantidad_represent
