#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import persona
from applications.agis.modules.db import tipo_pago

def definir_tabla():
    db=current.db
    T=current.T
    persona.definir_tabla()
    tipo_pago.definir_tabla()
    if not hasattr( db, 'pago' ):
        db.define_table( 'pago',
            Field( 'persona_id','reference persona' ),
            Field( 'tipo_pago_id','reference tipo_pago' ),
            Field( 'cantidad','double' ),
            Field( 'codigo_recivo','string',length=10 ),
            )
        db.pago.persona_id.label=T( 'Avona' )
        db.pago.tipo_pago_id.label=T( 'Tipo de pago' )
        db.pago.cantidad.label=T( 'Cantidad' )
        db.pago.cantidad.requires.append( IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) )
        db.pago.codigo_recivo.label=T( 'Código recivo' )
        db.pago.codigo_recivo.requires=IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) )
        db.commit()
