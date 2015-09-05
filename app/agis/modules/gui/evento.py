# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import evento as evento_model

__doc__ = """Herramientas de GUI para eventos"""

def seleccionar(context, tipo = '1', estado = True):
    """Muestra GRID para seleccionar un evento"""
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    evento_model.definir_tabla() # definir los modelos si no se ha hecho ya
    context.asunto = T('Seleccione el evento')
    query = (db.evento.id > 0)
    if context.ano_academico:
        # Si se nos da un año académico concreto entonces mostrar solo los
        # eventos de ese año académico.
        query &= (db.ano_academico_id == context.ano_academico.id)
    else:
        # Si solo tenemos la unidad organica buscar todos los eventos que se
        # desarrolan en la misma.
        assert context.unidad_organica != None
        tmp = db(
            db.ano_academico.unidad_organica_id == context.unidad_organica.id
            ).select(db.ano_academico.id)
        annos = [i['id'] for i in tmp]
        query &= db.evento.ano_academico_id.belongs(annos)
    query &= (db.evento.tipo == tipo)
    query &= (db.evento.estado == estado)
    context.manejo = tools.selector(query,
        [db.evento.nombre], 'evento_id')
    response.title = T('Eventos')
    response.subtitle = context.unidad_organica.nombre
    return context
