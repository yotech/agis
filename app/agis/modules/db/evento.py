#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from gluon import *
from applications.agis.modules.db import ano_academico
from applications.agis.modules import tools

EVENTO_TIPO_VALUES={
    '1':'Inscripción',
}

def evento_tipo_represent( valor,fila ):
    T=current.T
    return T( EVENTO_TIPO_VALUES[ valor ] )

def obtener_manejo():
    db=current.db
    definir_tabla()
    db.evento.id.readable=False
    return tools.manejo_simple( db.evento )

def eventos_activos(tipo='1'):
    definir_tabla()
    hoy = (datetime.now()).date()
    db = current.db
    query=((db.evento.tipo==tipo) &
           (db.evento.estado==True) &
           ((str(hoy) >= db.evento.fecha_inicio) & (str(hoy) <= db.evento.fecha_fin))
          )
    return db(query).select()

def definir_tabla():
    db=current.db
    T=current.T
    ano_academico.definir_tabla()
    if not hasattr( db,'evento' ):
        db.define_table( 'evento',
            Field( 'nombre','string',length=10 ),
            Field( 'tipo','string',length=1 ),
            Field( 'fecha_inicio','date' ),
            Field( 'fecha_fin','date' ),
            Field( 'ano_academico_id','reference ano_academico' ),
            Field( 'estado','boolean',default=True ),
            format="%(nombre)s",
            )
        db.evento.nombre.label=T( 'Nombre' )
        db.evento.nombre.requires = [ IS_NOT_EMPTY( error_message=T( 'Información requerida' ) ) ]
        db.evento.nombre.requires.append(
            IS_NOT_IN_DB( db,'evento.nombre',error_message=T( 'Ya existe' ) )
            )
        db.evento.tipo.label=T( 'Tipo de evento' )
        db.evento.tipo.requires=IS_IN_SET( EVENTO_TIPO_VALUES,zero=None )
        db.evento.tipo.represent=evento_tipo_represent
        db.evento.fecha_inicio.label=T( 'Inicio' )
        db.evento.fecha_fin.label=T( 'Fin' )
        db.evento.fecha_inicio.requires.append( IS_NOT_EMPTY( error_message=T( 'Información requerida' ) ) )
        db.evento.fecha_fin.requires.append( IS_NOT_EMPTY( error_message=T( 'Información requerida' ) ) )
        db.evento.ano_academico_id.label=T( 'Año académico' )
        db.commit()
