# -*- coding: utf-8 -*-
from datetime import datetime
from gluon import *
from gluon.storage import Storage
from agiscore import tools
from agiscore.db import unidad_organica
from agiscore.db import escuela

def obtener_manejo():
    db = current.db
    db.ano_academico.id.readable = False
    return tools.manejo_simple(db.ano_academico, [db.ano_academico.nombre])

def ano_actual():
    ahora = datetime.now()
    return str(ahora.year)

def buscar_actual(unidad_organica_id = None):
    db = current.db
    # para evitar la recursividad con definir_tabla
    if not hasattr( db,'ano_academico' ): definir_tabla()
    if not unidad_organica_id:
        unidad_organica_id = (escuela.obtener_sede_central()).id
    actual_nombre = ano_actual()
    query = ((db.ano_academico.nombre == actual_nombre) &
             (db.ano_academico.unidad_organica_id == unidad_organica_id))
    return db(query).select().first()

def ano_academico_format(registro):
    return registro.nombre

def definir_tabla():
    db = current.db
    T = current.T
    unidad_organica.definir_tabla()
    if not hasattr(db, 'ano_academico'):
        tbl = db.define_table('ano_academico',
            Field('nombre', 'string',length=4,required=True ),
            Field('descripcion', 'text',length=200,required=False ),
            Field('meses', 'list:integer', default=[]),
            Field('multa', 'integer', default=10), # porciento de multa
            # dia del mes a partir del cual se comienza a aplicar el porciento
            # de multa.
            Field('dia_limite', 'integer', default=11),
            Field('unidad_organica_id', 'reference unidad_organica'),
            format=ano_academico_format,
            )
        tbl.nombre.requires = [ IS_INT_IN_RANGE(1900, 2300,
            error_message=T('Año incorrecto, debe estar entre 1900 y 2300')
            )]
        tbl.nombre.requires.extend( tools.requerido )
        tbl.nombre.comment = T('En el formato AAAA')
        tbl.nombre.label = T('Año Académico')
        tbl.descripcion.label = T('Descripción')
        tbl.descripcion.requires = [IS_UPPER()]
        tbl.unidad_organica_id.label = T('Unidad Orgánica')
        tbl.multa.label = T('Multa(%)')
        tbl.multa.comment = T("""
            % de recargo que se aplicará como multa después de pasado el Día Límite
        """)
        tbl.multa.requires = IS_INT_IN_RANGE(1, 101)
        tbl.dia_limite.label = T('Día Límite')
        tbl.dia_limite.comment = T("""
            Día del mes a partir del cual se comienza a aplicar la multa por
            concepto de retraso en el Pago de Propina.
        """)
        tbl.dia_limite.requires = IS_INT_IN_RANGE(1, 32)
        # db.commit()
