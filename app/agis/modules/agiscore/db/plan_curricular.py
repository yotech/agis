#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore.db import carrera_uo
from agiscore.db import nivel_academico
from agiscore.db import asignatura
from agiscore import tools

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
    return list(
        set([i.id for i in db((db.plan_curricular.estado==True) &
                              (db.plan_curricular.carrera_id.belongs(carreras))).select()])
     )

def obtenerAsignaturasAcceso(carrera_id):
    """Retorna los ids de las asignaturas en el nivel ACCESO para una carrera"""
    # planes activos para la carrera
    planes = obtener_para_carreras([carrera_id])
    from agiscore.db.asignatura_plan import asignaturas_por_planes
    from agiscore.db.nivel_academico import ACCESO
    asignaturas = asignaturas_por_planes(planes, nivel=ACCESO)
    return [a.id for a in asignaturas]

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

def seleccionar(context):
    """Genera un GRID para la selección de un plan de una carrera

    En context debe estar la carrera de la cual se selecionará un plan
    """
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    context.asunto = T('Seleccione el plan acádemico')
    query = (db.plan_curricular.id > 0)
    query &= (db.plan_curricular.carrera_id == context.carrera_uo.id)
    context.manejo = tools.selector(query,
        [db.plan_curricular.nombre, db.plan_curricular.estado],
        'plan_curricular_id')
    return context

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
        db.plan_curricular.carrera_id.label=T( 'Carrera' )
        db.plan_curricular.carrera_id.required=True
        db.plan_curricular.estado.label=T( '¿Activo?' )
        db.plan_curricular.estado.represent=plan_curricular_estado_represent
        db.commit()
