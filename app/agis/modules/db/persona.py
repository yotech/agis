#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import comuna
from applications.agis.modules.db import municipio
from applications.agis.modules.db import provincia
from applications.agis.modules.db import tipo_documento_identidad
from applications.agis.modules.tools import requerido

PERSONA_GENERO_VALUES = { 'M': 'Masculino','F':'Femenino' }
def persona_genero_represent(valor, fila):
    return current.T( PERSONA_GENERO_VALUES[ valor ] )

PERSONA_ESTADO_CIVIL_VALUES = { 'S':'Soltero','C':'Casado','D':'Divorsiado','O':'Otro' }
def persona_estado_civil_represent(valor, fila):
    return current.T( PERSONA_ESTADO_CIVIL_VALUES[valor] )

PERSONA_ESTADO_POLITICO_VALUES = { 'P':'Policia','C':'Civil','M':'Militar', }
def persona_estado_politico_represent( valor,fila ):
    return current.T( PERSONA_ESTADO_POLITICO_VALUES[ valor ] )

def definir_tabla():
    db = current.db
    T = current.T
    comuna.definir_tabla()
    municipio.definir_tabla()
    provincia.definir_tabla()
    tipo_documento_identidad.definir_tabla()
    if not hasattr(db, 'persona'):
        db.define_table('persona',
            Field( 'nombre','string',length=15,required=True ),
            Field( 'apellido1','string', length=15,required=True ),
            Field( 'apellido2','string',length=15,required=True ),
            Field( 'fecha_nacimiento','date',required=True ),
            Field( 'genero','string',length=1 ),
            Field( 'lugar_nacimiento','reference comuna',required=True ),
            Field( 'estado_civil','string',length=1 ),
            Field( 'tipo_documento_identidad_id','reference tipo_documento_identidad' ),
            Field( 'numero_identidad','string',length=20,required=True ),
            Field( 'nombre_padre','string',length=50,required=True ),
            Field( 'nombre_madre','string',length=50,required=True ),
            Field( 'estado_politico','string',length=1,default='C' ),
            Field( 'nacionalidad','string',length=50,required=True ),
            Field( 'dir_provincia_id', 'reference provincia',required=True ),
            Field( 'dir_municipio_id', 'reference municipio',required=True ),
            Field( 'dir_comuna_id','reference comuna',required=True ),
            Field( 'direccion','text',length=300,required=False ),
            Field( 'telefono','string',length=20,required=False ),
            Field( 'email','string', length=20,required=False ),
            Field( 'nombre_completo',
                compute=lambda r: "{0} {1} {2}".format(r.nombre,r.apellido1,r.apellido2),
                label=T('Nombre completo')
            ),
            format="%(nombre_completo)s",
        )
        db.persona.nombre.requires = requerido
        db.persona.apellido1.requires,db.persona.apellido2.requires = ( requerido,requerido )
        db.persona.nombre_padre.requires,db.persona.nombre_madre.requires = ( requerido, requerido )
        db.persona.numero_identidad.requires = requerido
        db.persona.apellido1.label = T( 'Primer apellido' )
        db.persona.apellido2.label = T( 'Segundo apellido' )
        db.persona.fecha_nacimiento.label = T( 'Fecha de nacimiento' )
        db.persona.fecha_nacimiento.requires = []
        db.persona.fecha_nacimiento.requires.extend( requerido )
        db.persona.fecha_nacimiento.requires.append( IS_DATE() )
        db.persona.lugar_nacimiento.label = T( 'Lugar de nacimiento' )
        db.persona.tipo_documento_identidad_id.label = T('Documento de identidad')
        db.persona.numero_identidad.label = T( 'Número de identidad' )
        db.persona.nombre_padre.label = T( 'Nombre del padre' )
        db.persona.nombre_madre.label = T( 'Nombre de la madre' )
        db.persona.nacionalidad.label = T( 'Nacionalidad' )
        db.persona.estado_politico.label = T( 'Estado político' )
        db.persona.dir_comuna_id.label = T( 'Comuna' )
        db.persona.dir_municipio_id.label = T( 'Municipio' )
        db.persona.dir_provincia_id.label = T( 'Provincia' )
        db.persona.direccion.label = T( 'Dirección' )
        db.persona.telefono.label = T( 'Teléfono de contacto' )
        db.persona.email.label = T( 'E-Mail' )
        db.persona.genero.represent = persona_genero_represent
        db.persona.genero.requires = IS_IN_SET( PERSONA_GENERO_VALUES,zero=None )
        db.persona.estado_civil.represent = persona_estado_civil_represent
        db.persona.estado_civil.requires = IS_IN_SET( PERSONA_ESTADO_CIVIL_VALUES,zero=None )
        db.persona.estado_politico.represet = persona_estado_politico_represent
        db.persona.estado_politico.requires = IS_IN_SET( PERSONA_ESTADO_POLITICO_VALUES,zero=None )
        db.persona.nacionalidad.widget = SQLFORM.widgets.autocomplete(current.request,
            db.persona.nacionalidad,limitby=(0,10),min_length=3
            )
        db.commit()
