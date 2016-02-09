# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import examen
from agiscore.db import estudiante

# def obtenerResultadosAccesoGenerales(candidatura_id, evento_id):
#     """
#     retorna la media alcanzada por el estudiante en en los examenes realizados
# 
#     :param candidatura_id: int
#     :param evento_id: int
#     :return: float
#     """
#     db = current.db
#     cand = db.candidatura(candidatura_id)
#     lista_examenes = examen.generar_examenes_acceso(cand, evento_id)
#     cantidad = len(lista_examenes)
#     if cantidad == 0:
#         return 0.0
#     suma = 0
#     for e in lista_examenes:
#         crear_entradas(e)
#         n = db.nota(examen_id=e, estudiante_id=cand.estudiante_id)
#         r = 0
#         if n:
#             if n.valor is not None:
#                 r = n.valor
#         suma += r
#     return float(suma) / cantidad

def obtenerResultadosAcceso(candidatura_id, carrera_id, evento_id):
    """Retorna la media de resultados de los examenes de acceso para la
    canidatura en la carrera especificada.
    """
    db = current.db
#     cand = db(db.candidatura.id == candidatura_id).select(cache=(current.cache.ram, 300),
#                                                           cacheable=True).first()
#     est = db(db.estudiante.id == cand.estudiante_id).select(cache=(current.cache.ram, 300),
#                                                             cacheable=True).first()
    est = db.estudiante(db.candidatura(candidatura_id).estudiante_id)
    examenes = examen.examenesAccesoPorCarrera(carrera_id, evento_id)

    suma = 0
    cantidad = len(examenes)
    if cantidad == 0:
        return 0.0
    for e in examenes:
        # chequear que las entradas existan
#         crear_entradas(e.id)
        n = db.nota(examen_id=e.id, estudiante_id=est.id)
        r = 0
        if n:
            if n.valor is not None:
                r = n.valor
        suma += r
    med = float(suma) / cantidad
    return med

# -- iss124 Para mostrar un grid solo con los datos necesarios de los
#    estudiantes.
def crear_entradas(examen_id):
    """Crea las entradas por defecto para las notas"""
    db = current.db
    # definir_tabla()
    candidatos = examen.obtener_candidaturas(examen_id)
    # convertir los ids de candidatos en ids de estudiantes
    e_ids = [db.candidatura(c.id).estudiante_id for c in candidatos]
    # crear los registros solo para los que no tienen ya uno.
    if len(e_ids) != db(db.nota.examen_id == examen_id).count():
        for e_id in e_ids:
            r = db.nota(estudiante_id=e_id, examen_id=examen_id)
            if r is None:
                # si no hay nota para el estudiantes crear un registro de nota vacio
                db.nota.insert(estudiante_id=e_id, examen_id=examen_id)

def valor_represent(v, fila):
    return v if v != None else 'N/D'

def nota_format(fila):
    return valor_represent(fila.valor, fila)

def definir_tabla():
    db = current.db
    T = current.T
    examen.definir_tabla()
    estudiante.definir_tabla()
    if not hasattr(db, 'nota'):
        db.define_table('nota',
            Field('valor', 'float', default=None),
            Field('examen_id', 'reference examen'),
            Field('estudiante_id', 'reference estudiante'))
        db.nota.valor.label = T('Nota')
        db.nota.valor.requires = IS_FLOAT_IN_RANGE(0, 21,
            error_message=T('Debe ser un valor entre 0 y 20'))
        db.nota.valor.represent = valor_represent
        db.nota.examen_id.label = T('Examen')
        db.nota.estudiante_id.label = T('Estudiante')
        db.nota.id.readable = False
        db.commit()
