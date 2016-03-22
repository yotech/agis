#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from agiscore.db import comuna
from agiscore.db import municipio
from agiscore.db import provincia
from agiscore.db import pais
from agiscore.db import tipo_documento_identidad
from agiscore.tools import requerido

PERSONA_GENERO_VALUES = { 'M': 'MASCULINO', 'F':'FEMININO' }
def persona_genero_represent(valor, fila):
    return current.T(PERSONA_GENERO_VALUES[ valor ])

PERSONA_ESTADO_CIVIL_VALUES = {'S':'SOLTEIRO(A)',
                               'C':'CASADO(A)',
                               'D':'DIVORCIADO(A)',
                               'O':'OUTRO' }
def persona_estado_civil_represent(valor, fila):
    return current.T(PERSONA_ESTADO_CIVIL_VALUES[valor])

PERSONA_ESTADO_POLITICO_VALUES = { 'P':'POLICIA', 'C':'CIVIL', 'M':'MILITAR', }
def persona_estado_politico_represent(valor, fila):
    return current.T(PERSONA_ESTADO_POLITICO_VALUES[ valor ])

SITUACION_MILITAR_VALUES = {'1': 'SIM',
                            '2': 'NÃO',
                            '3': 'NÃO APLICÁVEL'}
def situacion_militar_represent(valor, fila):
    v = valor
    if not (valor in SITUACION_MILITAR_VALUES.keys()):
        v = '3'
    return SITUACION_MILITAR_VALUES[v]

def obtener_por_uuid(uuid):
    definir_tabla()
    db = current.db
    q = (db.persona.uuid == uuid)
    return db(q).select(db.persona.ALL).first()

def esconder_campos():
    visibilidad(False)
def mostrar_campos():
    visibilidad(True)

def visibilidad(valor):
    """Cambia la propiedad readable de todos los campos de persona"""
    db = current.db
    definir_tabla()
    for f in db.persona:
        f.readable = False

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
        last_name="{} {}".format(p.apellido1 if p.apellido1 is not None else "",
                                 p.apellido2),
        email=p.email,
        password=db.auth_user.password.validate(tmppass)[0])
    db.commit()
    p.user_id = user_id
    p.update_record()
    db.commit()

def _after_insert(f, id):
    db = current.db
    p = db.persona(id)
    # -- si tiene un correo valido crear el el usuario
    if p.email:
        crear_usuario(p)

    n_completo = __nombre_completo(p)
    p.update_record(nombre_completo=n_completo)

def _after_update(s, f):
    db = current.db
    p = s.select().first()
    # -- si la persona no tenia un usuario asociado crearlo
    # cuando se le ponga un email valido.
    if p.email and not p.user_id:
        crear_usuario(p)
    n_completo = __nombre_completo(p)
    s.update_naive(nombre_completo=n_completo)

    # chequear que si es un estudiante se debe actualizar su NM
    if 'genero' in f.keys():
        if p.estudiante.select().first() is not None:
            db.estudiante.actualizar_sexo_en_nm(p)

    return None
# --iss129: cambiar los widgets por defecto para cumplir con el limite de
#           caracteres.
def my_string_widget(field, value):
    w = SQLFORM.widgets.string.widget(field, value, _maxlength=field.length)
    return w
# --

# --iss129: calcular el nombre completo solo con la primera letra del
#           primer apellido
def __nombre_completo(r):
    c = r.nombre + " "
    if r.apellido1 and (r.apellido1 != ""):
        c += r.apellido1[0] + ". "
    c += r.apellido2
    return c
# --

# TODO: actualizar el usuario asociado si se cambia el correo electrónico
def definir_tabla():
    db = current.db
    T = current.T
    comuna.definir_tabla()
    municipio.definir_tabla()
    provincia.definir_tabla()
    pais.definir_tabla()
    tipo_documento_identidad.definir_tabla()
    if not hasattr(db, 'persona'):
        tbl = db.define_table('persona',
            Field('nombre', 'string', length=30, label=T("Nombre")),
            # iss129: el primer apellido puede ser omitido
            Field('apellido1', 'string', length=30, label=T("Primer apellido")),
            Field('apellido2', 'string', length=30,
                  label=T("Segundo apellido")),
            Field('fecha_nacimiento', 'date', label=T("Fecha de nacimiento")),
            Field('genero', 'string', length=1, label=T('Género')),
            Field('nombre_padre', 'string', length=250,
                  label=T('Nombre del padre')),
            Field('nombre_madre', 'string', length=250,
                  label=T('Nombre de la madre')),
            Field('pais_origen', 'reference pais', label=T("País de origen")),
            Field('lugar_nacimiento', 'reference comuna',
                  label=T("Lugar de nacimiento")),
            Field('estado_civil', 'string', length=1, label=T("Estado civil")),
            Field('tipo_documento_identidad_id',
                  'reference tipo_documento_identidad',
                  label=T('Documento de identidad')),
            Field('numero_identidad', 'string', length=20,
                  label=T('Número de identidad')),
            Field('estado_politico', 'string', length=1, default='C',
                  label=T('Estado militar')),
            Field('situacion_militar', 'string', length=1, default='1',
                  label=T("¿Receseamento Militar?"),),
            Field('pais_residencia', 'reference pais',
                  label=T("País de residencia")),
            Field('dir_comuna_id', 'reference comuna', label=T("Localidad")),
            Field('direccion', 'text', length=300, label=T("Dirección")),
            Field('telefono', 'string', length=20, label=T("Teléfono")),
            Field('telefono_alternativo', 'string', length=20,
                  label=T("Teléfono alternativo")),
            # --iss129: email puede ser de más de 20 caracteres.
            Field('email', 'string', length=50, required=False),
            Field('user_id', 'reference auth_user',
                  notnull=False,
                  required=False,
                  default=None),
            Field('nombre_completo', 'string', length=100,
                  compute=__nombre_completo, label=T('Nombre completo')),
            db.my_signature,
            format="%(nombre_completo)s",
        )
        tbl._after_insert.append(_after_insert)
        tbl._after_update.append(_after_update)
        tbl.telefono.label = T('Teléfono de contacto')
        # -- iss168: el número de telefono debe ser unico entre las personas
        tbl.telefono.requires = IS_EMPTY_OR(
            IS_NOT_IN_DB(db, 'persona.telefono',
                         error_message=T('Value already in database')))
        # -------
        # -- no repetir numeros de identidad
        tbl.numero_identidad.requires = IS_NOT_IN_DB(db,
                                                     'persona.numero_identidad')
        # ---------------------------------------------------------------------
        tbl.email.label = T('E-Mail')
        tbl.genero.represent = persona_genero_represent
        tbl.genero.requires = IS_IN_SET(
            PERSONA_GENERO_VALUES, zero=None)
        tbl.estado_civil.represent = persona_estado_civil_represent
        tbl.estado_civil.requires = IS_IN_SET(
            PERSONA_ESTADO_CIVIL_VALUES, zero=None)
        tbl.estado_politico.represet = persona_estado_politico_represent
        tbl.estado_politico.requires = IS_IN_SET(
            PERSONA_ESTADO_POLITICO_VALUES, zero=None)
        tbl.situacion_militar.represent = situacion_militar_represent
        tbl.situacion_militar.requires = IS_IN_SET(
            SITUACION_MILITAR_VALUES, zero=None)
        tbl.id.readable = False
        tbl.user_id.readable = False
        tbl.user_id.writable = False
