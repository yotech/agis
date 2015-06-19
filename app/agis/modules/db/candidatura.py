#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import estudiante
from applications.agis.modules.db import tipos_ensennanza
from applications.agis.modules.db import escuela_media
from applications.agis.modules.tools import requerido
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import discapacidad
from applications.agis.modules.db import regimen
from applications.agis.modules.db import regimen_uo
from applications.agis.modules.db import ano_academico

CANDIDATURA_DOCUMENTOS_VALUES = {
    '1':'Certificado original',
    '2':'Cópia de documento',
    '3':'Documento de trabajo',
    '4':'Documento Militar',
    '5':'Internado',
}
def candidatura_documentos_represent(valor, fila):
    return current.T( CANDIDATURA_DOCUMENTOS_VALUES[ valor ] )

def candidatura_format(registro):
    db = current.db
    definir_tabla()
    est = db.estudiante[registro.estudiante_id]
    return estudiante.estudiante_format(est)

def definir_tabla():
    db = current.db
    T = current.T
    estudiante.definir_tabla()
    tipos_ensennanza.definir_tabla()
    escuela_media.definir_tabla()
    unidad_organica.definir_tabla()
    discapacidad.definir_tabla()
    regimen.definir_tabla()
    regimen_uo.definir_tabla()
    ano_academico.definir_tabla()
    if not hasattr( db,'candidatura' ):
        db.define_table( 'candidatura',
            Field( 'estudiante_id','reference estudiante' ),
            # laborales
            Field( 'es_trabajador','boolean' ),
            Field( 'profesion','string',length=30 ),
            Field( 'nombre_trabajo','string',length=30 ),
            # procedencia
            Field( 'habilitacion','string',length=5 ),
            Field( 'tipo_escuela_media_id','reference tipo_escuela_media' ),
            Field( 'escuela_media_id','reference escuela_media' ),
            Field( 'carrera_procedencia','string',length=20 ),
            Field( 'anno_graduacion','string',length=4 ),
            # institucional
            Field( 'unidad_organica_id', 'reference unidad_organica' ),
            Field( 'discapacidades', 'list:reference discapacidad' ),
            Field( 'documentos', 'list:string' ),
            Field( 'regimen_unidad_organica_id', 'reference regimen_unidad_organica' ),
            Field( 'ano_academico_id','reference ano_academico' ),
            format=candidatura_format,
            )
        db.candidatura.estudiante_id.label = T( 'Estudiante' )
        db.candidatura.estudiante_id.required = True
        db.candidatura.habilitacion.required = True
        db.candidatura.habilitacion.widget = SQLFORM.widgets.autocomplete(
            current.request,db.candidatura.habilitacion,limitby=(0,10),min_length=1
        )
        db.candidatura.tipo_escuela_media_id.label = T( 'Tipo de enseñanza media de procedencia' )
        db.candidatura.tipo_escuela_media_id.required = True
        db.candidatura.escuela_media_id.label = T( 'Escuela de procedencia' )
        db.candidatura.escuela_media_id.required = True
        db.candidatura.carrera_procedencia.label = T( 'Carrera de procedencia' )
        db.candidatura.carrera_procedencia.required = True
        db.candidatura.carrera_procedencia.requires = requerido
        db.candidatura.anno_graduacion.label = T( 'Año de conclusión' )
        db.candidatura.anno_graduacion.requires = [ IS_INT_IN_RANGE(1900, 2300,
            error_message=T( 'Año incorrecto, debe estar entre 1900 y 2300' )
            )]
        db.candidatura.anno_graduacion.requires.extend( requerido )
        db.candidatura.unidad_organica_id.required = True
        db.candidatura.discapacidades.required = False
        db.candidatura.discapacidades.notnull = False
        db.candidatura.discapacidades.label = T( 'Necesita educación especial' )
        db.candidatura.documentos.requires = IS_IN_SET( CANDIDATURA_DOCUMENTOS_VALUES,multiple=True )
        db.candidatura.documentos.represent = candidatura_documentos_represent
        db.candidatura.documentos.label = T( 'label' )
        db.candidatura.unidad_organica_id.label = T( 'Unidad organica' )
        db.candidatura.regimen_unidad_organica_id.label = T( 'Régimen' )
        db.candidatura.ano_academico_id.label = T( 'Año académico' )
        db.candidatura.ano_academico_id.default = ano_academico.buscar_actual().id
        db.commit()
