#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import nivel_academico
from applications.agis.modules.db import asignatura
from applications.agis.modules import tools

def obtener_manejo( enlaces ):
    definir_tabla()
    db=current.db
    db.plan_curricular.id.readable=False
    return tools.manejo_simple( db.plan_curricular,enlaces=enlaces )

def plan_curricular_estado_represent( valor,fila ):
    T=current.T
    return T('Si') if valor else T('No')


def definir_tabla():
    db=current.db
    T=current.T
    carrera_uo.definir_tabla()
    nivel_academico.definir_tabla()
    asignatura.definir_tabla()
    if not hasattr( db,'plan_curricular' ):
        db.define_table( 'plan_curricular',
            Field( 'nombre','string',length=30 ),
            Field( 'carrera_id','reference carrera_uo' ),
            Field( 'estado','boolean',default=False ),
            format="%(nombre)s",
            )
        db.plan_curricular.nombre.label=T( 'Nombre del plan' )
        db.plan_curricular.nombre.requires=[ IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) ]
        db.plan_curricular.carrera_id.label=T( 'Carrera' )
        db.plan_curricular.carrera_id.required=True
        db.plan_curricular.estado.label=T( '¿Activo?' )
        db.plan_curricular.estado.represent=plan_curricular_estado_represent
        db.commit()
