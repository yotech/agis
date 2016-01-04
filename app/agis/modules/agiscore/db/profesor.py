#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore.db import persona
from agiscore.db import departamento
from agiscore import tools

PROFESOR_VINCULO_VALUES = {
        '1':'EFECTIVO',
        '2':'COLABORADOR',
        '3':'OTRO',
    }
def profesor_vinculo_represent(valor, fila):
    T = current.T
    return T(PROFESOR_VINCULO_VALUES[ valor ])

PROFESOR_CATEGORIA_VALUES = {
        '1':'PROFESOR INSTRUCTOR',
        '2':'PROFESOR ASISTENTE',
        '3':'PROFESPR AUXILIAR',
        '4':'PROFESOR ASOCIADO',
        '5':'PROFESOR TITULAR',
        '6':'OTRO',
    }
def profesor_categoria_represent(valor, fila):
    T = current.T
    return T(PROFESOR_CATEGORIA_VALUES[ valor ])

PROFESOR_GRADO_VALUES = {
    '1':'BACHILLER',
    '2':'LICENCIADO',
    '3':'MASTER',
    '4':'DOCTOR',
}
def profesor_grado_represent(valor, fila):
    T = current.T
    return T(PROFESOR_GRADO_VALUES[ valor ])

def obtener_profesores(dpto=None):
    """retorna un query con las condiciones establecidas por los parametros
    para la selección de varios profesores
    """
    db = current.db
    q = (db.persona.uuid == db.profesor.uuid)
    if dpto:
        q &= (db.profesor.departamento_id == dpto.id)
    return q

def personas_a_profesores(personas):
    """Dada una lista de ID's de personas retornar la lista de profesores que
    corresponden"""
    if not isinstance(personas, (list, tuple)):
        personas = [personas]
    return [persona_a_profesor(id) for id in personas]

def persona_a_profesor(persona_id):
    """Dado un id de persona retornar el profesor que corresponde"""
    db = current.db
    definir_tabla()
    return db(db.profesor.persona_id == persona_id).select().first()

def obtener_manejo(enlaces=[], detalles=False):
    definir_tabla()
    db = current.db
    conjunto = obtener_profesores()
    manejo = tools.manejo_simple(conjunto,
        crear=False, editable=False, buscar=True,
        orden=[db.persona.nombre_completo],
        campos=[db.persona.nombre_completo,
                db.profesor.categoria,
                db.profesor.departamento_id],
        enlaces=enlaces,
        detalles=detalles,
        )
    return manejo

def profesor_format(fila):
    db = current.db
    definir_tabla()
    p = db.persona[fila.persona_id]
    return p.nombre_completo

def verificar_grupos(user_id):
    db = current.db
    auth = current.auth
    conf = current.conf
    if user_id:
        # si tiene asignado un usuario valido agregar membresia al grupo
        # de profesores sino la tiene ya
        role = conf.take('roles.profesor')
        if not auth.has_membership(user_id=user_id, role=role):
            role = db.auth_group(role=role)
            auth.add_membership(group_id=role.id, user_id=user_id)

def copia_uuid_callback(valores):
    """Se llama antes de insertar un valor en la tabla

    En este caso lo estamos usando para copiar el UUID de la persona
    """
    db = current.db
    p = db.persona(valores['persona_id'])
    valores['uuid'] = p.uuid
    if p.user_id:
        # si tiene asignado un usuario valido agregar membresia al grupo
        # de profesores
        verificar_grupos(p.user_id)

def _after_update(s, f):
    db = current.db
    pro = s.select().first()
    p = db.persona(uuid=pro.uuid)
    if p.user_id:
        verificar_grupos(p.user_id)

def definir_tabla():
    db = current.db
    T = current.T
    persona.definir_tabla()
    departamento.definir_tabla()
    if not hasattr(db, 'profesor'):
        db.define_table('profesor',
            Field('persona_id', 'reference persona'),
            Field('vinculo', 'string', length=1),
            Field('categoria', 'string', length=1),
            Field('grado', 'string', length=1),
            Field('fecha_entrada', 'date'),
            Field('departamento_id', 'reference departamento'),
            db.my_signature,
            format=profesor_format,
        )
        db.profesor.id.readable = False
        db.profesor._before_insert.append(copia_uuid_callback)
        db.profesor._after_update.append(_after_update)
        db.profesor.persona_id.label = T('Nombre')
        db.profesor.persona_id.writable = False
        db.profesor.vinculo.label = T('Vinculo')
        db.profesor.vinculo.represent = profesor_vinculo_represent
        db.profesor.vinculo.requires = IS_IN_SET(PROFESOR_VINCULO_VALUES, zero=None)
        db.profesor.vinculo.default = '1'
        db.profesor.categoria.label = T('Categoría docente')
        db.profesor.categoria.represent = profesor_categoria_represent
        db.profesor.categoria.requires = IS_IN_SET(PROFESOR_CATEGORIA_VALUES, zero=None)
        db.profesor.categoria.default = '1'
        db.profesor.grado.label = T('Grado científico')
        db.profesor.grado.represent = profesor_grado_represent
        db.profesor.grado.requires = IS_IN_SET(PROFESOR_GRADO_VALUES, zero=None)
        db.profesor.grado.default = '2'
        db.profesor.fecha_entrada.label = T('Fecha entrada')
        db.profesor.fecha_entrada.comment = T('Fecha de entrada a la Unidad Organica')
        db.profesor.fecha_entrada.required = True
        db.profesor.fecha_entrada.requires.append(
            IS_NOT_EMPTY(error_message=current.T('Información requerida')),
            )
        db.profesor.departamento_id.label = T('Departamento')
        db.profesor.departamento_id.requires = IS_IN_DB(db, 'departamento.id', '%(nombre)s', zero=None)
        db.commit()
