#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import persona
from applications.agis.modules.db import departamento

PROFESOR_VINCULO_VALUES = {
    '1':'Efectivo',
    '2':'Colaborador',
    '3':'Otro',
}
def profesor_vinculo_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_VINCULO_VALUES[ valor ] )

PROFESOR_CATEGORIA_VALUES = {
    '1':'Profesor Instructor',
    '2':'Profesor Asistente',
    '3':'Profesor Auxiliar',
    '4':'Profesor Asociado',
    '5':'Profesor titular',
    '6':'Otro',
}
def profesor_categoria_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_CATEGORIA_VALUES[ valor ] )

PROFESOR_GRADO_VALUES = {
    '1':'Bachiller',
    '2':'Licenciado',
    '3':'Master',
    '4':'Doctor',
}
def profesor_grado_represent( valor,fila ):
    T  = current.T
    return T( PROFESOR_GRADO_VALUES[ valor ] )

def obtener_profesores():
    """retorna el set de persona que son profesores"""
    db = current.db
    return (db.persona.id == db.profesor.persona_id)

def obtener_manejo():
    definir_tabla()
    db = current.db
    conjunto = obtener_profesores()
    manejo = SQLFORM.grid(query=conjunto,
        fields=[db.persona.nombre_completo,db.profesor.categoria,db.profesor.departamento_id],
        orderby=[db.persona.nombre_completo],
        details=False,
        csv=False,
        searchable=True,
        editable=False,
        showbuttontext=False,
        maxtextlength=100,
        formstyle='bootstrap',
    )
    return manejo

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
        )
        db.profesor.persona_id.label=T( 'Persona' )
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
