#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore.db import plan_curricular
from agiscore.db import asignatura
from agiscore.db import nivel_academico
from agiscore import tools

def asignaturas_posibles( plan_id ):
    definir_tabla()
    db = current.db
    row = db(db.asignatura_plan.plan_curricular_id==None).select(
        db.asignatura.ALL,db.asignatura_plan.ALL,
        left=db.asignatura_plan.on((db.asignatura.id==db.asignatura_plan.asignatura_id)
                                   &(db.asignatura_plan.plan_curricular_id==plan_id)),
        orderby=db.asignatura.nombre)
    pos = []
    for item in row:
        pos.append( (item.asignatura.id, item.asignatura.nombre) )
    return pos

def asignaturas_por_planes( planes, nivel = None ):
    """Dada una lista de ID's de planes retorna la lista de las asignaturas asociadas a estos"""
    db = current.db
    definir_tabla()
    q = db.asignatura_plan.plan_curricular_id.belongs(planes)
    q &= (db.asignatura.id == db.asignatura_plan.asignatura_id)
    if nivel:
        q &= (db.asignatura_plan.nivel_academico_id == db.nivel_academico.id)
        q &= (db.nivel_academico.nivel == nivel)
    return db(q).select(db.asignatura.id,db.asignatura.nombre,distinct=True)

def obtener_manejo( plan_id ):
    request = current.request
    db = current.db
    T = current.T
    definir_tabla()
    db.asignatura_plan.id.readable=False
    db.asignatura_plan.plan_curricular_id.writable=False
    db.asignatura_plan.plan_curricular_id.readable=False
    db.asignatura_plan.plan_curricular_id.default=plan_id
    posibles = asignaturas_posibles(plan_id)
    if ('new' in current.request.args) and (not posibles):
        current.session.flash = T(
            """No es posible asignar más asignaturas a este plan o no se han
            definino más asignaturas"""
            )
        redirect(URL(c=request.controller,
                     f=request.function,
                     vars=request.vars))
    db.asignatura_plan.asignatura_id.requires = IS_IN_SET(posibles, zero=None)
    query=((db.asignatura_plan.id > 0) &
           (db.asignatura_plan.plan_curricular_id == plan_id) )
    return tools.manejo_simple(query, buscar=True,
        campos=[db.asignatura_plan.nivel_academico_id,
                db.asignatura_plan.asignatura_id]
        )

def seleccionar(context):
    """GRID de selección de asignaturas, context debe contener
    el plan académico al que pertenece la asignatura
    """
    assert isinstance(context, Storage)
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    context.asunto = T('Seleccione la asignatura')
    query = (db.asignatura_plan.id > 0)
    query &= (db.asignatura_plan.plan_curricular_id == context.plan_curricular.id)
    query &= (db.asignatura_plan.asignatura_id == db.asignatura.id)
    context.manejo = tools.selector(query,
        [db.asignatura_plan.asignatura_id],
        'asignatura_plan_id')
    return context

def definir_tabla():
    db=current.db
    T=current.T
    plan_curricular.definir_tabla()
    asignatura.definir_tabla()
    nivel_academico.definir_tabla()
    if not hasattr( db,'asignatura_plan' ):
        db.define_table( 'asignatura_plan',
            Field( 'plan_curricular_id','reference plan_curricular' ),
            Field( 'asignatura_id','reference asignatura' ),
            Field( 'nivel_academico_id','reference nivel_academico' ),
            format="",
            )
        db.asignatura_plan.plan_curricular_id.label=T( 'Plan curricular' )
        db.asignatura_plan.asignatura_id.label=T( 'Asignatura' )
        db.asignatura_plan.nivel_academico_id.label=T( 'Nivel académico' )
        db.commit()
