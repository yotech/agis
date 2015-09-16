# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules.db import examen
from applications.agis.modules.db import estudiante

# -- iss124 Para mostrar un grid solo con los datos necesarios de los 
#    estudiantes.
def crear_entradas(examen_id):
    """Crea las entradas por defecto para las notas"""
    db = current.db
    definir_tabla()
    candidatos = examen.obtener_candidaturas(examen_id)
    # convertir los ids de candidatos en ids de estudiantes
    e_ids = [db.candidatura(c.id).estudiante_id for c in candidatos]
    # crear los registros solo para los que no tienen ya uno.
    for e_id in e_ids:
        q  = (db.nota.estudiante_id == e_id)
        q &= (db.nota.examen_id == examen_id)
        r = db(q).select().first()
        if not r:
            # si no hay nota para el estudiantes crear un registro de nota vacio
            db.nota.insert(estudiante_id=e_id, examen_id=examen_id)
            db.commit()
    
def valor_represent(v, fila):
    return v if v != None else 'N/D'

def definir_tabla():
    db = current.db
    T = current.T
    examen.definir_tabla()
    estudiante.definir_tabla()
    if not hasattr(db, 'nota'):
        db.define_table('nota',
            Field('valor', 'integer', default=None),
            Field('examen_id', 'reference examen'),
            Field('estudiante_id', 'reference estudiante'))
        db.nota.valor.label = T('Nota')
        db.nota.valor.requires = IS_INT_IN_RANGE(0, 21,
            error_message=T('Debe ser un valor entre 0 y 20'))
        db.nota.valor.represent = valor_represent
        db.nota.examen_id.label = T('Examen')
        db.nota.estudiante_id.label = T('Estudiante')
        db.nota.id.readable = False
        db.commit()
