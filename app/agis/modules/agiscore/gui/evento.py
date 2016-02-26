# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore import tools
from agiscore.db import evento as evento_model
from agiscore.validators import IS_DATE_GT

__doc__ = """Herramientas de GUI para eventos"""

# Registro de controladores para cada tipo de evento
controllers_register = {
    evento_model.INSCRIPCION: 'inscripcion',
    evento_model.MATRICULA: 'matricula',
    evento_model.CMATRICULA: 'cmatricula',
    evento_model.ENORMAL: 'enormal',
    evento_model.CAPOSPRAZO: 'caposprazo'}
    
def form_configurar_evento(record,
                           back_url,
                           db=None,
                           request=None,
                           T=None):
    # configurar campos
    if db is None:
        db = current.db
    if request is None:
        request = current.request
    if T is None:
        T = current.T
    tbl = db.evento
    tbl.id.readable = False
    tbl.nombre.writable = False
    tbl.nombre.readable = False
    tbl.tipo.readable = False
    tbl.tipo.writable = False
    tbl.ano_academico_id.writable = False
    tbl.ano_academico_id.readable = False
    
    if request.vars.fecha_inicio:
        # validar que la fecha de inicio este antes que la de fin
        (fecha_inicio, msg) = db.evento.fecha_inicio.validate(
            request.vars.fecha_inicio)
        if msg is None:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(),
                                            IS_DATE_GT(minimum=fecha_inicio)]
        else:
            db.evento.fecha_fin.requires = [IS_NOT_EMPTY(), IS_DATE()]
    
    form = SQLFORM(db.evento, record=record, submit_button=T("Guardar"))
    form.add_button(T("Cancelar"), back_url)
    
    return form

def seleccionar_evento(ano_academico_id=None,
                unidad_organica_id=None,
                tipo='1',
                estado=True):
    """Muestra GRID para seleccionar un evento"""
    request = current.request
    T = current.T
    db = current.db
    evento_model.definir_tabla()  # definir los modelos si no se ha hecho ya
    query = (db.evento.id > 0)
    if ano_academico_id:
        # Si se nos da un año académico concreto entonces mostrar solo los
        # eventos de ese año académico.
        query &= (db.ano_academico_id == ano_academico_id)
    else:
        # Si solo tenemos la unidad organica buscar todos los eventos que se
        # desarrolan en la misma.
        assert unidad_organica_id != None
        tmp = db(
            db.ano_academico.unidad_organica_id == unidad_organica_id
            ).select(db.ano_academico.id)
        annos = [i['id'] for i in tmp]
        query &= db.evento.ano_academico_id.belongs(annos)
    query &= (db.evento.tipo == tipo)
    query &= (db.evento.estado == estado)
    m = tools.selector(query,
        [db.evento.nombre], 'evento_id')
    co = CAT()
    heading = DIV(T("Seleccionar evento"), _class="panel-heading")
    body = DIV(m, _class="panel-body")
    co.append(DIV(heading, body, _class="panel panel-default"))
    return co
