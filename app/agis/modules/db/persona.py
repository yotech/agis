#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from applications.agis.modules.db import comuna
from applications.agis.modules.db import municipio
from applications.agis.modules.db import provincia
from applications.agis.modules.db import tipo_documento_identidad
from applications.agis.modules.tools import requerido

PERSONA_GENERO_VALUES = { 'M': 'MASCULINO','F':'FEMENINO' }
def persona_genero_represent(valor, fila):
    return current.T( PERSONA_GENERO_VALUES[ valor ] )

PERSONA_ESTADO_CIVIL_VALUES = {'S':'SOLTERO(A)',
                               'C':'CASADO(A)',
                               'D':'DIVORCIADO(A)',
                               'O':'OTRO' }
def persona_estado_civil_represent(valor, fila):
    return current.T( PERSONA_ESTADO_CIVIL_VALUES[valor] )

PERSONA_ESTADO_POLITICO_VALUES = { 'P':'POLICIA','C':'CIVIL','M':'MILITAR', }
def persona_estado_politico_represent( valor,fila ):
    return current.T( PERSONA_ESTADO_POLITICO_VALUES[ valor ] )

def obtener_por_uuid(uuid):
    definir_tabla()
    db = current.db
    q = (db.persona.uuid == uuid)
    return db(q).select(db.persona.ALL).first()

def crear_usuario(p):
    """Dado una registro de persona crea un usuario para la misma
    Antes de llamar a este método el usuario debe tener asociado un correo
    electronico.
    """
    db = current.db
    assert p.email != None
    import md5
    tmppass = md5.md5(p.uuid).hexdigest()
    user_id = db.auth_user.insert(
        first_name=p.nombre,
        last_name=p.apellido1,
        email=p.email,
        password=db.auth_user.password.validate(tmppass)[0])
    db.commit()
    p.user_id = user_id
    p.update_record()
    db.commit()

# TODO: actualizar el usuario asociado si se cambia el correo electrónico

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
            Field('tipo_documento_identidad_id',
                  'reference tipo_documento_identidad'),
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
            Field('user_id', 'reference auth_user',
                  notnull=False,
                  required=False,
                  default=None),
            Field( 'nombre_completo',
                compute=lambda r: "{0} {1} {2}".format(r.nombre,
                                                       r.apellido1,
                                                       r.apellido2),
                label=T('Nombre completo')
            ),
            db.my_signature,
            format="%(nombre_completo)s",
        )
        db.persona.nombre.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.nombre.requires.append(IS_UPPER())
        db.persona.apellido1.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.apellido2.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.apellido1.requires.append(IS_UPPER())
        db.persona.apellido2.requires.append(IS_UPPER())
        db.persona.nombre_padre.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.nombre_padre.requires.append(IS_UPPER())
        db.persona.nombre_madre.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.nombre_madre.requires.append(IS_UPPER())
        db.persona.numero_identidad.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.numero_identidad.requires.append(IS_UPPER())
        db.persona.numero_identidad.requires.append(
            IS_NOT_IN_DB(db,'persona.numero_identidad'))
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
        db.persona.genero.label = T( 'Género' )
        db.persona.genero.represent = persona_genero_represent
        db.persona.genero.requires = IS_IN_SET(
            PERSONA_GENERO_VALUES, zero=None)
        db.persona.estado_civil.represent = persona_estado_civil_represent
        db.persona.estado_civil.requires = IS_IN_SET(
            PERSONA_ESTADO_CIVIL_VALUES, zero=None )
        db.persona.estado_politico.represet = persona_estado_politico_represent
        db.persona.estado_politico.requires = IS_IN_SET(
            PERSONA_ESTADO_POLITICO_VALUES, zero=None )
        db.persona.nacionalidad.requires = [
            IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
        db.persona.nacionalidad.requires.append(IS_UPPER())
        db.persona.nacionalidad.widget = SQLFORM.widgets.autocomplete(current.request,
            db.persona.nacionalidad,limitby=(0,10),min_length=3,distinct=True
            )
        db.persona.id.readable = False
        db.persona.user_id.readable = False
        db.persona.user_id.writable = False
        db.commit()
