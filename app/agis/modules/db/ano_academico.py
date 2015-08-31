#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import escuela

def seleccionar(context):
    assert isinstance(context, Storage)
    assert (context.unidad_organica != None)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    response.flash = T('Seleccione un año académico')
    query = ((db.ano_academico.id > 0) &
        (db.ano_academico.unidad_organica_id == context.unidad_organica.id))
    context.manejo = tools.selector(query,
        [db.ano_academico.nombre], 'ano_academico_id')
    response.title = T('Años académicos')
    response.subtitle = context.unidad_organica.nombre
    return context

def obtener_manejo():
    db = current.db
    db.ano_academico.id.readable = False
    return tools.manejo_simple(db.ano_academico, [db.ano_academico.nombre])

def ano_actual():
    ahora = datetime.now()
    return str(ahora.year)

def buscar_actual(unidad_organica_id = None):
    db = current.db
    if not hasattr( db,'ano_academico' ): definir_tabla() # para evitar la recursividad con definir_tabla
    if not unidad_organica_id:
        unidad_organica_id = (escuela.obtener_sede_central()).id
    actual_nombre = ano_actual()
    query = ((db.ano_academico.nombre == actual_nombre) &
             (db.ano_academico.unidad_organica_id == unidad_organica_id))
    return db(query).select().first()

class AnoNombreValidator(object):

    def __init__(self, error_message="Ya existe ese año académico en la UO"):
        T = current.T
        self.e = T(error_message)

    def validate(self, value):
        db = current.db
        request = current.request
        if not 'unidad_organica_id' in request.vars:
            self.e = ""
            return False
        if not request.vars.unidad_organica_id:
            self.e = ""
            return False
        unidad_organica_id = int(request.vars.unidad_organica_id)
        hay = db((db.ano_academico.nombre == value) &
                 (db.ano_academico.unidad_organica_id == unidad_organica_id)).select()
        if hay:
            if 'edit' in request.args:
                return True # si se esta editando
            else:
                return False

        return True

    def parsed(self, value):
        return value

    def __call__(self, value):
        if self.validate(value):
            return (self.parsed(value), None)
        else:
            return (value, self.e)

def ano_academico_format(registro):
    #db = current.db
    #T = current.T
    #uo = db.unidad_organica[registro.unidad_organica_id]
    #return '{0} - {1}'.format(registro.nombre, uo.nombre)
    return registro.nombre

def definir_tabla():
    db = current.db
    T = current.T
    unidad_organica.definir_tabla()
    if not hasattr( db,'ano_academico' ):
        db.define_table( 'ano_academico',
            Field( 'nombre','string',length=4,required=True ),
            Field( 'descripcion','text',length=200,required=False ),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format=ano_academico_format,
            )
        db.ano_academico.nombre.requires = [ IS_INT_IN_RANGE(1900, 2300,
            error_message=T( 'Año incorrecto, debe estar entre 1900 y 2300' )
            ), AnoNombreValidator()]
        db.ano_academico.nombre.requires.extend( tools.requerido )
        db.ano_academico.nombre.comment = T( 'En el formato AAAA' )
        db.ano_academico.nombre.label = T( 'Año Académico' )
        db.ano_academico.descripcion.label = T( 'Descripción' )
        db.ano_academico.descripcion.requires = [IS_UPPER()]
        db.ano_academico.unidad_organica_id.label = T('Unidad Orgánica')
        db.commit()
