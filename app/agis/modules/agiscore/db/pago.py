#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import persona
from agiscore.db import tipo_pago

FORMA_PAGO_VALORES={
    '1':'BANCO',
    '2':'TARGETA'
}
def forma_pago_represent(valor, fila):
    T=current.T
    return T( FORMA_PAGO_VALORES[valor] )

def cantidad_avonada(persona, concepto):
    """Dado el id de una persona calcula la suma total de sus pago dado un
    concepto
    """
    db = current.db
    sum = db.pago.cantidad.sum()
    query = (db.pago.persona_id == persona.id)
    query &= (db.pago.tipo_pago_id == concepto.id)
    total = db(query).select(sum).first()[sum]
    if total is None:
        total = 0.0
        
    return total

def definir_tabla():
    db=current.db
    T=current.T
    persona.definir_tabla()
    tipo_pago.definir_tabla()
    if not hasattr( db, 'pago' ):
        db.define_table( 'pago',
            Field( 'persona_id','reference persona' ),
            Field( 'tipo_pago_id','reference tipo_pago' ),
            Field( 'forma_pago','string',length=1 ),
            Field( 'numero_transaccion','string',length=20 ),
            Field( 'cantidad','double' ),
            Field( 'codigo_recivo','string',length=10 ),
            )
        db.pago.forma_pago.label=T( 'Forma de pago' )
        db.pago.forma_pago.requires = IS_IN_SET( FORMA_PAGO_VALORES,zero=None )
        db.pago.forma_pago.represent=forma_pago_represent
        db.pago.numero_transaccion.label=T( 'Número de transacción' )
        db.pago.numero_transaccion.requires= [IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) )]
        db.pago.numero_transaccion.requires.append(
            IS_NOT_IN_DB(db, 'pago.numero_transaccion')
            )
        db.pago.persona_id.label=T( 'Avona' )
        db.pago.tipo_pago_id.label=T( 'Tipo de pago' )
        db.pago.cantidad.label=T( 'Cantidad' )
        db.pago.cantidad.requires.append( IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) )
        db.pago.codigo_recivo.label=T( 'Código recivo' )
        db.pago.codigo_recivo.requires=[IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) )]
        db.pago.codigo_recivo.requires.append(
            IS_NOT_IN_DB(db, 'pago.codigo_recivo')
            )
        db.commit()
