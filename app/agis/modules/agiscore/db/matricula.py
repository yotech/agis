# -*- coding: utf-8 -*-
from gluon import current
from gluon import Field
from gluon.validators import IS_IN_SET
from agiscore.db import ano_academico
from agiscore.db import estudiante, nivel_academico
from agiscore.db import turma, regimen_uo, plan_curricular
from agiscore.db import carrera_uo, especialidad

SITUACION_VALUES = {
    '1': '1ª Matrìcula-Novo',
    '2': 'Aprovado em toda-ano anterior',
    '3': 'Aprovado com Cadeiras em atraso',
    '4': 'Repetentes',
    '5': 'Transferencia',
    '7': 'Reprovado',
    '9': 'Licença por Doença',
    '10': 'Continuante bacharelato',
    '11': 'Estagio',
    '12': 'Preparação de tessis'
}

ESTADO_UO_VALUES = {
    '1': 'SEM MATRICULAR COM DÍVIDA',
    '2': 'SEM MATRICULAR',
    '3': 'MATRICULADO COM DÍVIDAS',
    '4': 'MATRICULADO',
}
SIN_MATRICULAR_CON_DEUDA = '1'
SIN_MATRICULAR = '2'
MATRICULADO_CON_DEUDAS = '3'
MATRICULADO = '4'

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T
    
    ano_academico.definir_tabla()
    estudiante.definir_tabla()
    carrera_uo.definir_tabla()
    regimen_uo.definir_tabla()
    plan_curricular.definir_tabla()
    nivel_academico.definir_tabla()
    especialidad.definir_tabla(db, T)
    turma.definir_tabla(db, T)
    # matricula
    if not hasattr(db, 'matricula'):
        tbl = db.define_table('matricula',
            Field('estudiante_id', 'reference estudiante'),
            Field('ano_academico_id', 'reference ano_academico'),
            Field('nivel', 'reference nivel_academico'),
            Field('situacion', 'string', length=1),
            Field('estado_uo', 'string', length=1),
            Field('regimen_id', 'reference regimen_unidad_organica'),
            Field('turma_id', 'reference turma'),
            Field('carrera_id', 'reference carrera_uo'),
            Field('espacialidad_id', 'reference especialidad'),
            Field('plan_id', 'reference plan_curricular'))
        
        # labels
        tbl.estudiante_id.label = T('Estudiante')
        tbl.ano_academico_id.label = T("Año académico")
        tbl.nivel.label = T("Nivel")
        tbl.situacion.label = T("Situación académica")
        tbl.estado_uo.label = T("Estado en la UO")
        tbl.regimen_id.label = T("Régimen")
        tbl.turma_id.label = T("Grupo")
        tbl.carrera_id.label = T("Carrera")
        tbl.plan_id.label = T("Plan curricular")
        tbl.espacialidad_id.label = T("Especialidad")
        
        tbl.estudiante_id.represent = lambda v,f: estudiante.estudiante_format(db.estudiante(v))
        
        tbl.situacion.requires = IS_IN_SET(SITUACION_VALUES, zero=None)
        tbl.situacion.represent = lambda v,f: SITUACION_VALUES[v]
        
        tbl.estado_uo.requires = IS_IN_SET(ESTADO_UO_VALUES, zero=None)
        tbl.estado_uo.default = SIN_MATRICULAR
        tbl.estado_uo.represent = lambda v,f: ESTADO_UO_VALUES[v]
        
    if not hasattr(db, 'arrastre'):
        tbl = db.define_table("arrastre",
            Field('matricula_id', 'reference matricula'),
            Field('asignaturas', 'list:reference asignatura')
            )
        
        tbl.matricula_id.label = T("Matricula")
        tbl.asignaturas.label = T("Arrastre")
        tbl.asignaturas.comment = T("""
        Seleccionar asignaturas que arrastra el estudiante
        """)
    
    if not hasattr(db, 'repitensia'):
        tbl = db.define_table("repitensia",
            Field('matricula_id', 'reference matricula'),
            Field('asignaturas', 'list:reference asignatura')
            )
        
        tbl.matricula_id.label = T("Matricula")
        tbl.asignaturas.label = T("Asignaturas")
        tbl.asignaturas.comment = T("""
        Seleccionar asignaturas que repite el estudiante
        """)
