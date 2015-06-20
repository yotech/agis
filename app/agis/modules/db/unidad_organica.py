#!/usr/bin/env python
# -*- coding: utf-8 -*-
import escuela
import provincia

from gluon import *

NIVELES = {
    '1': 'Sede central',
    '2': 'Unidad organica',
}
def nivel_agregacion_represent(valor, registro):
    return current.T(NIVELES[valor])
CLASIFICACIONES = {
            '20': 'Instituto Superior',
            '21': 'Instituto Técnico Superior',
            '22': 'Instituto Politécnico',
            '30': 'Escuela Superior',
            '31': 'Escuela Superior Técnica',
            '32': 'Escuela Superior Politécnica',
            '40': 'Academia',
            '50': 'Facultad',
            '60': 'Departamento',
            '70': 'Centro de Investigación Científica',
        }
def clasificacion_represent(valor, registro):
    return current.T(CLASIFICACIONES[valor])

def obtener_por_escuela(escuela_id=1):
    db = current.db
    definir_tabla()
    return db((db.unidad_organica.id > 0) & (db.unidad_organica.escuela_id == escuela_id)).select()

def widget_selector(escuela_id=None,callback=None):
    """
    Retorna un widget que permite seleccionar una unidad organica.

    Callback es la función/controlador a llamar cuando se seleccione una unidad organica
             el valor seleccionado es pasado como argumento a esa funcion. Si se define
             debe ser una tupla de tipo ('controller','function')
    """
    request = current.request
    if not escuela_id:
        escuela_id = escuela.obtener_escuela()
    if callback:
        c, f = callback
    else:
        c = request.controller
        f = request.function
    lista = obtener_por_escuela(escuela_id=escuela_id)
    if 'unidad_organica_id' in request.vars:
        seleccionado = request.vars.unidad_organica_id
    else:
        seleccionado = lista[0].id
    selector = SELECT(_id='widget_selector_uo',_name='unidad_organica_id')
    for uo in lista:
        op = None
        if int(seleccionado) == uo.id:
            op = OPTION(uo.nombre, _value=uo.id, _selected=True)
        else:
            op = OPTION(uo.nombre, _value=uo.id)
        selector.append(op)
    return XML(current.response.render('widget_selector.html',dict(selector=selector,c=c,f=f)))

def calcular_codigo(r):
    db = current.db
    escuela = db.escuela[r['escuela_id']]
    return (escuela.codigo +
        r['nivel_agregacion'] +
        r['clasificacion'] +
        r['codigo_registro']
    )

def obtener_sede_central(escuela_id):
    db = current.db
    if not escuela_id:
        raise HTTP(404)
    query = ((db.unidad_organica.escuela_id == escuela_id) & (db.unidad_organica.nivel_agregacion == '1'))
    return db(query).select().first()

def definir_tabla():
    db = current.db
    T = current.T
    escuela.definir_tabla()
    provincia.definir_tabla()
    if not hasattr(db, 'unidad_organica'):
        db.define_table('unidad_organica',
            Field('codigo',compute=calcular_codigo,notnull=True,label=T('Código'),),
            Field('nombre','string',required=True,notnull=True,length=100,label=T('Nombre'),),
            Field('direccion','text',required=False,notnull=False,label=T('Dirección'),),
            Field('nivel_agregacion','string',required=True,length=1,
                label=T('Nivel de agregación'),),
            Field('clasificacion','string',length=2,required=True,
                label=T('Clasificación'),),
            Field('codigo_registro','string',length=3,required=True,
                label=T('Código de registro'),
                comment=T("Código de registro en el Ministerio de Educación"),),
            Field('codigo_escuela', 'string',length=2,required=True,notnull=True,
                label=T('Código en la Escuela'),
                comment=T("Código de registro asignado por la Escuela"),),
            # referencias
            Field('escuela_id', 'reference escuela',required=True,
                label=T('Escuela'),),
            Field('provincia_id', 'reference provincia',label=T('Provincia')),
            # -----------
            format='%(nombre)s',
            singular=T('Unidad Organica'),
            plural=T('Unidades Organicas'),
        )
        db.unidad_organica.nivel_agregacion.requires = IS_IN_SET(NIVELES,zero=None)
        db.unidad_organica.nivel_agregacion.represent = nivel_agregacion_represent
        db.unidad_organica.clasificacion.requires = IS_IN_SET(CLASIFICACIONES,zero=None)
        db.unidad_organica.clasificacion.represent = clasificacion_represent
        db.unidad_organica.codigo_registro.requires = [
            IS_NOT_EMPTY(error_message=T('Se require el código de registro')),
            IS_MATCH('^\d{3,3}$', error_message=T('No es un código valido')),
            IS_NOT_IN_DB(db,'unidad_organica.codigo_registro'),
        ]
        db.unidad_organica.codigo_escuela.requires = [
            IS_NOT_EMPTY(error_message=T('Se requiere el código asignado por la escuela')),
            IS_MATCH('^\d{2,2}$', error_message=T('No es un código valido')),
            IS_NOT_IN_DB(db,'unidad_organica.codigo_escuela',
                error_message=T('Ya existe una UO con ese código'),
            ),
        ]
        db.unidad_organica.nombre.requires = IS_NOT_EMPTY(
            error_message=T('Se requiere un nombre'),
        )
        db.unidad_organica.provincia_id.requires = IS_IN_DB(db, 'provincia.id',
            '%(nombre)s',
            zero=T('Escoger provincia'),
        )
        db.unidad_organica.escuela_id.requires = IS_IN_DB(db, 'escuela.id',
            '%(nombre)s',
            zero=T('Escoger una escuela'),
        )

def obtener_manejo(escuela_id):
    """retorna un GRID para el manejo de las unidades organicas"""
    db = current.db
    T = current.T
    request = current.request
    if 'new' in request.args:
        db.unidad_organica.nivel_agregacion.default = '2'
        db.unidad_organica.nivel_agregacion.writable = False
        db.unidad_organica.escuela_id.default = escuela_id
        db.unidad_organica.escuela_id.writable = False
    query = ((db.unidad_organica.escuela_id == escuela_id) &
             (db.unidad_organica.nivel_agregacion == '2'))
    grid = SQLFORM.grid(query,
        fields=[db.unidad_organica.codigo,db.unidad_organica.nombre,
                db.unidad_organica.nivel_agregacion,
                db.unidad_organica.clasificacion,
                db.unidad_organica.provincia_id],
        csv=False,
        details=False,
        showbuttontext=False,
        formargs={'showid': False,'formstyle': 'bootstrap'},
    )
    return grid
