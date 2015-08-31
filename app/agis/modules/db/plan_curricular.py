#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import nivel_academico
from applications.agis.modules.db import asignatura
from applications.agis.modules import tools

class PlanCurricularNombreValidator(object):

    def __init__(self, error_message="Ya existe un plan con ese nombre para la carrera"):
        T = current.T
        self.e = T(error_message)

    def validate(self, value):
        db = current.db
        request = current.request
        #definir_tabla()
        if not 'carrera_uo_id' in request.vars:
            return False
        carrera_id = int(request.vars.carrera_uo_id)
        hay = db((db.plan_curricular.nombre == value) &
                 (db.plan_curricular.carrera_id == carrera_id)).select()
        if hay:
            return False

        return True

    def parsed(self, value):
        return value

    def __call__(self, value):
        if self.validate(value):
            return (self.parsed(value), None)
        else:
            return (value, self.e)

def obtener_para_carreras( carreras ):
    """Dada una lista de ID's de carreras retorna la lista de ID's de planes activos para estas"""
    db = current.db
    definir_tabla()
    return list(
        set([i.id for i in db((db.plan_curricular.estado==True) &
                              (db.plan_curricular.carrera_id.belongs(carreras))).select()])
     )

def obtener_manejo(enlaces=[], carrera_id=None):
    definir_tabla()
    db=current.db
    db.plan_curricular.id.readable=False
    query = db.plan_curricular
    if carrera_id:
        query = (db.plan_curricular.carrera_id == carrera_id)
    return tools.manejo_simple( query,enlaces=enlaces )

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
        db.plan_curricular.nombre.requires.append(IS_UPPER())
        db.plan_curricular.nombre.requires.append( PlanCurricularNombreValidator() )
        db.plan_curricular.carrera_id.label=T( 'Carrera' )
        db.plan_curricular.carrera_id.required=True
        db.plan_curricular.estado.label=T( '¿Activo?' )
        db.plan_curricular.estado.represent=plan_curricular_estado_represent
        db.commit()
