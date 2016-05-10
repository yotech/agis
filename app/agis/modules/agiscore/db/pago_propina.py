
# -*- coding: utf-8 -*-
import calendar
from datetime import date
import datetime
from gluon import *

from agiscore.db import persona
from agiscore.db import tipo_pago
from agiscore.db import pago
from agiscore.db.evento import ENORMAL, esta_activo
from agiscore.db.matricula import MATRICULADO, MATRICULADO_CON_DEUDAS

def check_propinas(db, ano, ev):
    # check all the estudiante on the current enormal event
    # for paiments
    hoy = datetime.date.today()
    mes_pivote = hoy.month - 1 if hoy.month - 1 > 0 else 1
    # ano = db.ano_academico(nombre=str(hoy.year))
    if ano is None:
        return

    # ev = db.evento(tipo=ENORMAL, ano_academico_id=ano.id)
    if ev is None:
        return

    unidad = db.unidad_organica(ano.unidad_organica_id)

    # regimen post laboral
    r_regular_q  = (db.regimen_unidad_organica.regimen_id == db.regimen.id)
    r_regular_q &= (db.regimen.codigo=='2')
    r_regular_q &= (db.regimen_unidad_organica.unidad_organica_id == unidad.id)
    r_regular = db(r_regular_q).select(db.regimen_unidad_organica.id).first()

    # Estudiantes que no tienen deuda... los que ya tienen deuda se mantienen
    # con el mismo estado
    tbl = db.estudiante
    query = (tbl.persona_id == db.persona.id)
    query &= (tbl.unidad_organica_id == unidad.id)
    query &= (tbl.id == db.matricula.estudiante_id)
    query &= (db.matricula.ano_academico_id == ano.id)
    query &= (db.matricula.regimen_id == r_regular.id)

    est_rows = db(query).select(db.persona.id, db.estudiante.id, db.matricula.id)
    for est in est_rows:
        estado = MATRICULADO_CON_DEUDAS
        m_matricua = db.matricula(est.matricula.id)
        # buscar los meses que se han pagado y analizar los meses por pagar
        query = (db.propina.persona_id == est.persona.id)
        query &= (db.propina.ano_academico_id == ano.id)
        rows = db(query).select(db.propina.mes,
            orderby=db.propina.mes,
            distinct=True)
        pagados = [row.mes for row in rows]
        meses_a_pagar = list(set(ano.meses) - set(pagados))
        # si ya tiene todos los meses pagados entonces no tener en cuenta para nada
        if set(meses_a_pagar) == set(pagados):
            estado = MATRICULADO
        if hoy.month in set(pagados):
            estado = MATRICULADO
        if (mes_pivote in set(pagados)) and (hoy.day <= ano.dia_limite):
            estado = MATRICULADO
        m_matricua.update_record(estado_uo=estado)
    db.commit()

    return

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
