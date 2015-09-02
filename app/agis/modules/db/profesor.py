#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules.db import persona
from applications.agis.modules.db import departamento
from applications.agis.modules import tools

PROFESOR_VINCULO_VALUES = {
        '1':'EFECTIVO',
        '2':'COLABORADOR',
        '3':'OTRO',
    }
def profesor_vinculo_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_VINCULO_VALUES[ valor ] )

PROFESOR_CATEGORIA_VALUES = {
        '1':'PROFESOR INSTRUCTOR',
        '2':'PROFESOR ASISTENTE',
        '3':'PROFESPR AUXILIAR',
        '4':'PROFESOR ASOCIADO',
        '5':'PROFESOR TITULAR',
        '6':'OTRO',
    }
def profesor_categoria_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_CATEGORIA_VALUES[ valor ] )

PROFESOR_GRADO_VALUES = {
    '1':'BACHILLER',
    '2':'LICENCIADO',
    '3':'MASTER',
    '4':'DOCTOR',
}
def profesor_grado_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_GRADO_VALUES[ valor ] )

def obtener_profesores():
    """retorna el set de persona que son profesores"""
    db = current.db
    return (db.persona.uuid == db.profesor.uuid)

def seleccionar(context):
    """Genera un GRID para la selección de un profesor

    En context debe estar el departamento donde se buscaran los
    profesores
    """
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    context.asunto = T('Seleccione el profesor')
    query = obtener_profesores()
    query &= (db.profesor.departamento_id == context.departamento.id)
    context.manejo = tools.selector(query,
        [db.profesor.grado, db.persona.nombre_completo],
        'profesor_id', tabla='profesor')
    response.title = context.departamento.nombre
    response.subtitle = T('Profesores')
    return context

def obtener_manejo(enlaces=[], detalles=False):
    definir_tabla()
    db = current.db
    conjunto = obtener_profesores()
    manejo = tools.manejo_simple(conjunto,
        crear=False, editable=False, buscar=True,
        orden=[db.persona.nombre_completo],
        campos=[db.persona.nombre_completo,
                db.profesor.categoria,
                db.profesor.departamento_id],
        enlaces=enlaces,
        detalles=detalles,
        )
    return manejo

def profesor_format(fila):
    db=current.db
    definir_tabla()
    p=db.persona[fila.persona_id]
    return p.nombre_completo

def copia_uuid_callback(valores):
    """Se llama antes de insertar un valor en la tabla

    En este caso lo estamos usando para copiar el UUID de la persona
    """
    db = current.db
    p = db.persona(valores['persona_id'])
    valores['uuid'] = p.uuid

def definir_tabla():
    db = current.db
    T = current.T
    persona.definir_tabla()
    departamento.definir_tabla()
    if not hasattr( db,'profesor' ):
        db.define_table( 'profesor',
            Field( 'persona_id','reference persona' ),
            Field( 'vinculo','string',length=1 ),
            Field( 'categoria','string',length=1 ),
            Field( 'grado','string',length=1 ),
            Field( 'fecha_entrada','date' ),
            Field( 'departamento_id','reference departamento' ),
            db.my_signature,
            format=profesor_format,
        )
        db.profesor.id.readable = False
        db.profesor._before_insert.append(copia_uuid_callback)
        db.profesor.persona_id.label=T( 'Nombre' )
        db.profesor.persona_id.writable=False
        db.profesor.vinculo.label=T( 'Vinculo' )
        db.profesor.vinculo.represent=profesor_vinculo_represent
        db.profesor.vinculo.requires=IS_IN_SET( PROFESOR_VINCULO_VALUES,zero=None )
        db.profesor.vinculo.default='1'
        db.profesor.categoria.label=T( 'Categoría docente' )
        db.profesor.categoria.represent=profesor_categoria_represent
        db.profesor.categoria.requires=IS_IN_SET( PROFESOR_CATEGORIA_VALUES,zero=None )
        db.profesor.categoria.default='1'
        db.profesor.grado.label=T( 'Grado científico' )
        db.profesor.grado.represent=profesor_grado_represent
        db.profesor.grado.requires=IS_IN_SET( PROFESOR_GRADO_VALUES,zero=None )
        db.profesor.grado.default='2'
        db.profesor.fecha_entrada.label=T( 'Fecha entrada' )
        db.profesor.fecha_entrada.comment=T( 'Fecha de entrada a la Unidad Organica' )
        db.profesor.fecha_entrada.required=True
        db.profesor.fecha_entrada.requires.append(
            IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ),
            )
        db.profesor.departamento_id.label=T( 'Departamento' )
        db.profesor.departamento_id.requires = IS_IN_DB( db,'departamento.id','%(nombre)s',zero=None )
        db.commit()
