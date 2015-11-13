#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import profesor
from agiscore.db import ano_academico
from agiscore.db import asignatura
from agiscore.db import evento
from agiscore import tools

def profesor_asignatura_format(fila):
    db=current.db
    definir_tabla()
    a = db.asignatura[fila.asignatura_id]
    p=profesor.profesor_format( db.profesor[fila.profesor_id] )
    return "{0} - {1}".format( p,a.nombre )

def obtener_manejo():
    db=current.db
    definir_tabla()
    db.profesor_asignatura.id.readable=False
    return tools.manejo_simple(db.profesor_asignatura)

def asignaturas_por_profesor(profesor_id,
        evento_id=None, ano_academico_id=None, estado=True):
    """Dado el ID de un profesor retornar la lista de asignaturas asignadas al
    mismo"""
    db = current.db
    definir_tabla()
    p = db.profesor(profesor_id)
    q = p.profesor_asignatura
    if evento_id:
        q &= (db.profesor_asignatura.evento_id == evento_id)
    if ano_academico_id:
        q &= (db.profesor_asignatura.ano_academico_id == ano_academico_id)
    q &= (db.profesor_asignatura.estado == estado)
    lista = [a.asignatura_id for a in p.profesor_asignatura.select()]
    return [db.asignatura(a) for a in lista]

def _before_delete(s):
    pass
    #db = current.db
    #conf = current.conf
    #rol_ja = conf.take('roles.jasignatura')
    #auth = current.auth
    #definir_tabla()
    #for r in s.select():
        #p = db.profesor(db.profesor_asignatura(r.id).profesor_id)
        #p = db.persona(uuid=p.uuid)
        #u = db.auth_user(p.user_id)
        #jrol = db.auth_group(role=rol_ja)
        #if auth.has_membership(role=rol_ja, user_id=u.id):
            #auth.del_membership(group_id=jrol.id, user_id=u.id)

def _after_update(s, f):
    pass
    #db = current.db
    #conf = current.conf
    #rol_ja = conf.take('roles.jasignatura')
    #auth = current.auth
    #definir_tabla()
    #if 'es_jefe' in f.keys():
        #pro = db.profesor(db.profesor_asignatura(f['id']).profesor_id)
        #p = db.persona(uuid=pro.uuid)
        #u = db.auth_user(p.user_id)
        #prol = db.auth_group(role=rol_ja)
        #if f['es_jefe']:
            ## verificar que tenga permiso de jefe de asignatura
            #if not auth.has_membership(role=rol_ja, user_id=u.id):
                #auth.add_membership(group_id=prol.id, user_id=u.id)
        #else:
            ## quitar permiso de jefe de asignatura si no esta marcado como
            ## jefe de asignatura en otras asignaciones.
            #if auth.has_membership(role=rol_ja, user_id=u.id):
                #for asignacion in pro.profesor_asignatura.select():
                    #if asignacion.es_jefe:
                        #return
                #auth.del_membership(group_id=prol.id, user_id=u.id)


def definir_tabla():
    db=current.db
    T=current.T
    profesor.definir_tabla()
    ano_academico.definir_tabla()
    asignatura.definir_tabla()
    if not hasattr(db, 'profesor_asignatura'):
        db.define_table( 'profesor_asignatura',
            Field( 'profesor_id','reference profesor' ),
            Field( 'ano_academico_id','reference ano_academico' ),
            Field( 'asignatura_id','reference asignatura' ),
            Field( 'evento_id','reference evento' ),
            Field( 'estado','boolean',default=True ),
            Field('es_jefe', 'boolean', default=False),
            format=profesor_asignatura_format,
            )
        db.profesor_asignatura.id.readable = False
        db.profesor_asignatura.profesor_id.label=T( 'Docente' )
        db.profesor_asignatura.ano_academico_id.label=T( 'Año académico' )
        db.profesor_asignatura.asignatura_id.label=T( 'Asignatura' )
        db.profesor_asignatura.evento_id.label=T( 'Evento' )
        db.profesor_asignatura.estado.label=T( 'Estado' )
        db.profesor_asignatura.es_jefe.label=T('¿Es Jefe de asignatura?')
        db.profesor_asignatura._after_update.append(_after_update)
        db.profesor_asignatura._before_delete.append(_before_delete)
        db.commit()
