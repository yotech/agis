#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import nivel_academico
from applications.agis.modules.db import asignatura
from applications.agis.modules import tools

def obtener_manejo():
    definir_tabla()
    db=current.db
    db.plan_curricular.id.readable=False
    return tools.manejo_simple( db.plan_curricular )


def definir_tabla():
    db=current.db
    T=current.T
    carrera_uo.definir_tabla()
    nivel_academico.definir_tabla()
    asignatura.definir_tabla()
    if not hasattr( db,'plan_curricular' ):
        db.define_table( 'plan_curricular',
            Field( 'carrera_id','reference carrera_uo' ),
            Field( 'nivel_academico_id','reference nivel_academico' ),
            Field( 'asignatura_id','reference asignatura' ),
            Field( 'estado','boolean',default=False ),
            )
        db.plan_curricular.carrera_id.label=T( 'Carrera' )
        db.plan_curricular.carrera_id.required=True
        db.plan_curricular.nivel_academico_id.label=T( 'Nivel académico' )
        db.plan_curricular.nivel_academico_id.required=True
        db.plan_curricular.nivel_academico_id.requires = IS_IN_DB( db,'nivel_academico.id','%(nombre)s',zero=None )
        db.plan_curricular.asignatura_id.label=T( 'Asignatura' )
        db.plan_curricular.asignatura_id.requires = IS_IN_DB( db,'asignatura.id','%(nombre)s',zero=None )
        db.plan_curricular.estado.label=T( '¿Activo?' )
        db.commit()
