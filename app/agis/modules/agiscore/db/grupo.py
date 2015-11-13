#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools
from agiscore.db import ano_academico
from agiscore.db import carrera_uo
from agiscore.db import nivel_academico
from agiscore.db import aula

def obtener_manejo():
    db = current.db
    definir_tabla()
    db.grupo.id.readable=False
    return tools.manejo_simple(db.grupo)

def definir_tabla():
    db = current.db
    T = current.T
    ano_academico.definir_tabla()
    carrera_uo.definir_tabla()
    nivel_academico.definir_tabla()
    aula.definir_tabla()
    if not hasattr(db, 'grupo'):
        db.define_table('grupo',
            Field('nombre', 'string', length=10),
            Field('ano_academico_id', 'reference ano_academico'),
            Field('carrera_id', 'reference carrera_uo'),
            Field('nivel_id','reference nivel_academico'),
            Field('aula_id','reference aula'),
            Field('estado','boolean'),
            )
        db.grupo.nombre.label = T('Nombre')
        db.grupo.nombre.requires = [ IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) ]
        db.grupo.nombre.requires.append(IS_UPPER())
        db.grupo.nombre.requires.append(IS_NOT_IN_DB(db,'grupo.nombre',error_message=T('Ya existe')))
        db.grupo.ano_academico_id.label = T('Año académico')
#         db.grupo.ano_academico_id.default = (ano_academico.buscar_actual()).id
        db.grupo.carrera_id.label = T('Carrera')
        db.grupo.nivel_id.label = T('Nivel académico')
        db.grupo.aula_id.label = T('Sala de aula')
        db.grupo.estado.label = T('Estado')
        db.commit()
