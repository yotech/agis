#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
from gluon import *
from agiscore.db import ano_academico
from agiscore import tools
from agiscore.validators import IS_DATE_GT

EVENTO_TIPO_VALUES = {
    '1':'INSCRIÇÃO',
    '2':'MATRÍCULA',
    '3':'CONFIRMAÇÃO MATRÍCULA',
}

INSCRIPCION = '1'
MATRICULA = '2'
CMATRICULA = '3'

def evento_tipo_represent(valor, fila):
    T = current.T
    return T(EVENTO_TIPO_VALUES[ valor ])

def conjunto(condiciones=None):
    definir_tabla()
    db = current.db
    query = (db.evento.id > 0)
    if condiciones:
        query &= condiciones
    return query

# def obtener_manejo(unidad_organica_id):
#     db = current.db
#     request = current.request
#     definir_tabla()
#     db.evento.id.readable = False
#     # preparar consulta
#     annos = db((db.ano_academico.id > 0) & 
#                (db.ano_academico.unidad_organica_id == unidad_organica_id)
#                ).select(db.ano_academico.ALL)
#     annos_ids = [a.id for a in annos]  # solo los ID's
#     if 'edit' in request.args:
# #         a_list = [(a.id, a.nombre) for a in annos]
# #         db.evento.ano_academico_id.requires = IS_IN_SET(
# #             a_list, zero=None)
#         (fecha_inicio, msg) = db.evento.fecha_inicio.validate(
#             request.vars.fecha_inicio)
#         if msg is None:
#             db.evento.fecha_fin.requires = [IS_NOT_EMPTY(),
#                                             IS_DATE_GT(minimum=fecha_inicio)]
#         else:
#             db.evento.fecha_fin.requires = [IS_NOT_EMPTY(), IS_DATE()]
#         # desactivar el resto de los campos
#         db.evento.nombre.writable = False
#         db.evento.ano_academico_id.writable = False
#         db.evento.tipo.writable = False
#     query = ((db.evento.id > 0) & 
#              (db.evento.ano_academico_id.belongs(annos_ids)))
#     db.evento.tipo.represent = evento_tipo_represent
#     return tools.manejo_simple(query, crear=False, borrar=False)

def esta_activo(e):
    """Si el evento cumple las condiciones para estar activo retorna True
    """
    hoy = date.today()
    
    if e.fecha_inicio is None:
        return False
    
    if e.fecha_fin is None:
        return False
    
    if (hoy >= e.fecha_inicio) and (hoy <= e.fecha_fin):
        return e.estado
    return False

# def eventos_activos(tipo='1'):
#     definir_tabla()
# #     hoy = (datetime.now()).date()
#     db = current.db
#     query = ((db.evento.tipo == tipo) & (db.evento.estado == True)  # &
# #            ((str(hoy) >= db.evento.fecha_inicio) & (str(hoy) <= db.evento.fecha_fin))
#           )
#     return db(query).select()

def opciones_evento(ano_academico_id):
    """Retorna una lista a ser usada con IS_IN_SET de eventos dado un
    año académico"""
    posibles = list()
    definir_tabla()
    db = current.db
    query = (db.evento.id > 0)
    query &= (db.evento.ano_academico_id == ano_academico_id)
    for e in db(query).select(db.evento.ALL, orderby=db.evento.nombre):
        posibles.append(
            (e.id, e.nombre)
            )
    return posibles

def crear_eventos(db, ano_academico_id):
    '''Crear los eventos de un año académico'''
    for k in EVENTO_TIPO_VALUES.keys():
        db.evento.insert(nombre=EVENTO_TIPO_VALUES[k],
                         tipo=k,
                         ano_academico_id=ano_academico_id,
                         estado=False)

def definir_tabla():
    db = current.db
    T = current.T
    ano_academico.definir_tabla()
    if not hasattr(db, 'evento'):
        db.define_table('evento',
            Field('nombre', 'string', length=50),
            Field('tipo', 'string', length=1),
            Field('fecha_inicio', 'date'),
            Field('fecha_fin', 'date'),
            Field('ano_academico_id', 'reference ano_academico'),
            Field('estado', 'boolean', default=True),
            format="%(nombre)s",
            )
        db.evento.nombre.label = T('Nombre')
        db.evento.nombre.requires = [ IS_NOT_EMPTY(error_message=T('Información requerida')) ]
        db.evento.nombre.requires.append(IS_UPPER())
        db.evento.nombre.requires.append(
            IS_NOT_IN_DB(db, 'evento.nombre', error_message=T('Ya existe'))
            )
        db.evento.tipo.label = T('Tipo de evento')
        db.evento.tipo.requires = IS_IN_SET(EVENTO_TIPO_VALUES, zero=None)
        # db.evento.tipo.represent=evento_tipo_represent
        db.evento.fecha_inicio.label = T('Inicio')
        db.evento.fecha_fin.label = T('Fin')
        db.evento.fecha_inicio.requires.append(IS_NOT_EMPTY(error_message=T('Información requerida')))
        db.evento.fecha_fin.requires.append(IS_NOT_EMPTY(error_message=T('Información requerida')))
        db.evento.ano_academico_id.label = T('Año académico')
        db.commit()
        # instalar los callback en año academico.
#         db.ano_academico._after_insert.append(_crear_eventos_defecto)
