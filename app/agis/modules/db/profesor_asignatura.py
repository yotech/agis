#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import profesor
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import evento
from applications.agis.modules import tools

def profesor_asignatura_format(fila):
    db=current.db
    definir_tabla()
    a = db.asignatura[fila.asignatura_id]
    p=profesor.profesor_format( db.profesor[fila.profesor_id] )
    return "{0} - {1}".format( p,a.nombre )

# def obtener_manejo():
#     db=current.db
#     definir_tabla()
#     db.profesor_asignatura.id.readable=False
#     return tools.manejo_simple

def definir_tabla():
    db=current.db
    T=current.T
    profesor.definir_tabla()
    ano_academico.definir_tabla()
    asignatura.definir_tabla()
    db.define_table( 'profesor_asignatura',
        Field( 'profesor_id','reference profesor' ),
        Field( 'ano_academico_id','reference ano_academico' ),
        Field( 'asignatura_id','reference asignatura' ),
        Field( 'evento_id','reference evento' ),
        Field( 'estado','boolean',default=True ),
        format=profesor_asignatura_format,
        )
    db.profesor_asignatura.profesor_id.label=T( 'Docente' )
    db.profesor_asignatura.ano_academico_id.label=T( 'Año académico' )
#     db.profesor_asignatura.ano_academico_id.default=(ano_academico.buscar_actual()).id
    db.profesor_asignatura.asignatura_id.label=T( 'Asignatura' )
    db.profesor_asignatura.evento_id.label=T( 'Evento' )
    db.profesor_asignatura.estado.label=T( 'Estado' )
