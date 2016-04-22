# -*- coding: utf-8 -*-
import calendar
from gluon import *

from agiscore.db import persona
from agiscore.db import tipo_pago
from agiscore.db import pago


def mes_represent(valor, fila):
    T = current.T
    return T(calendar.month_name[valor])

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T

    pago.definir_tabla(db, T)
    if not hasattr(db, 'propina'):
        tbl = db.define_table('propina',
            Field('pago_id', 'reference pago'),
            Field('mes', 'integer'),
        )
        tbl.mes.label = T("Mes")
        tbl.pago_id.label = T("Info. Pago")
        tbl.pago_id.readable = False
        tbl.mes.requires = IS_INT_IN_RANGE(1, 13)
        tbl.mes.represent = mes_represent
