#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from gluon import *
from agiscore.db import ano_academico
from agiscore import tools
from agiscore.validators import IS_DATE_GT

EVENTO_TIPO_VALUES = {
    '1':'INSCRIÇÃO',
    '2':'MATRÍCULA',
    '3':'CONFIRMAÇÃO MATRÍCULA',
    '4':'ÉPOCA NORMAL',
    '5':'CONFIRMAÇÃO APÓS O PRAZO',
}

INSCRIPCION = '1'
MATRICULA = '2'
CMATRICULA = '3'
ENORMAL = '4'
CAPOSPRAZO = '5'

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

# def opciones_evento(ano_academico_id):
#     """Retorna una lista a ser usada con IS_IN_SET de eventos dado un
#     año académico"""
#     posibles = list()
#     definir_tabla()
#     db = current.db
#     query = (db.evento.id > 0)
#     query &= (db.evento.ano_academico_id == ano_academico_id)
#     for e in db(query).select(db.evento.ALL, orderby=db.evento.nombre):
#         posibles.append(
#             (e.id, e.nombre)
#             )
#     return posibles

def crear_eventos(db, ano_academico_id):
    '''Crear los eventos de un año académico'''
    tipos = EVENTO_TIPO_VALUES.keys()
    tipos.sort()
    ano = int(db.ano_academico(ano_academico_id).nombre)
    # INSCRIPCION
    fecha_inicio = date(ano, 1, 1)
    fecha_fin = fecha_inicio + timedelta(30)
    db.evento.insert(nombre=EVENTO_TIPO_VALUES[INSCRIPCION],
        tipo=INSCRIPCION,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ano_academico_id=ano_academico_id,
        estado=False)
    # Confirmación de matrícula
    fecha_inicio = fecha_fin + timedelta(1)
    fecha_fin = fecha_inicio + timedelta(30)
    db.evento.insert(nombre=EVENTO_TIPO_VALUES[CMATRICULA],
        tipo=CMATRICULA,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ano_academico_id=ano_academico_id,
        estado=False)
    # Matrícula
    fecha_inicio = fecha_fin + timedelta(1)
    fecha_fin = fecha_inicio + timedelta(30)
    db.evento.insert(nombre=EVENTO_TIPO_VALUES[MATRICULA],
        tipo=MATRICULA,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ano_academico_id=ano_academico_id,
        estado=False)
    # Confirmación despues del plazo
    fecha_inicio = fecha_fin + timedelta(1)
    fecha_fin = fecha_inicio + timedelta(30)
    db.evento.insert(nombre=EVENTO_TIPO_VALUES[CAPOSPRAZO],
        tipo=CAPOSPRAZO,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ano_academico_id=ano_academico_id,
        estado=False)
    # epoca normal
    fecha_inicio = fecha_fin + timedelta(1)
    fecha_fin = fecha_inicio + timedelta(270)
    db.evento.insert(nombre=EVENTO_TIPO_VALUES[ENORMAL],
        tipo=ENORMAL,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ano_academico_id=ano_academico_id,
        estado=False)

def evento_format(row):
    db = current.db
    ano = db.ano_academico(row.ano_academico_id)
    represent = "{}".format(row.nombre)
    represent += " ({})".format(ano.nombre) if ano is not None else ""
    # return "{} ({})".format(row.nombre,
    #                        db.ano_academico(row.ano_academico_id).nombre)

    return represent

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
            format=evento_format,
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
