# -*- coding: utf-8 -*-
from gluon import *
from agiscore.gui.mic import Accion

def pago_link(cmp_id, persona_id, evento_id, activo=True, T=None):
    if T is None:
        T = current.T

    url = URL("pago_propina",
        "index.load",
        args=[evento_id, persona_id],
        user_signature=True)
    onclick = 'web2py_component("{}","{}")'
    l = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                        ' ',
                        T("Propina")),
                    '#',
                    activo,
                    _class="btn btn-default btn-sm",
                    _title=T("Realizar Pago de Propina"),
                    _onclick=onclick.format(url, cmp_id))

    return l
