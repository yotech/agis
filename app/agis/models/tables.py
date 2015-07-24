# -*- coding: utf-8 -*-
'''
Created on 18/5/2015

@author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
'''

from applications.agis.modules.db import region_academica
from applications.agis.modules.db import provincia
from applications.agis.modules.db import municipio
from applications.agis.modules.db import comuna
from applications.agis.modules.db import escuela
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import descripcion_carrera
from applications.agis.modules.db import regimen
from applications.agis.modules.db import tipos_ensennanza
from applications.agis.modules.db import escuela_media
from applications.agis.modules.db import tipo_documento_identidad
from applications.agis.modules.db import discapacidad
from applications.agis.modules.db import regimen_uo
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import persona
from applications.agis.modules.db import estudiante
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import candidatura_carrera
from applications.agis.modules.db import campus
from applications.agis.modules.db import edificio
from applications.agis.modules.db import aula
from applications.agis.modules.db import tipo_pago
from applications.agis.modules.db import departamento
from applications.agis.modules.db import profesor
from applications.agis.modules.db import nivel_academico
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import plan_curricular
from applications.agis.modules.db import plazas
from applications.agis.modules.db import evento
from applications.agis.modules.db import profesor_asignatura
from applications.agis.modules.db import asignatura_plan
from applications.agis.modules.db import grupo
from applications.agis.modules.db import pago
from applications.agis.modules.db import examen
#
# TODO: Depués de migrar todas las tablas a este formato comentar
#       esto y en cada vista solo llamar las tablas necesarias.
#
ano_academico.definir_tabla()
region_academica.definir_tabla()
provincia.definir_tabla()
municipio.definir_tabla()
comuna.definir_tabla()
escuela.definir_tabla()
unidad_organica.definir_tabla()
descripcion_carrera.definir_tabla()
regimen.definir_tabla()
tipos_ensennanza.definir_tabla()
escuela_media.definir_tabla()
tipo_documento_identidad.definir_tabla()
discapacidad.definir_tabla()
regimen_uo.definir_tabla()
carrera_uo.definir_tabla()
persona.definir_tabla()
estudiante.definir_tabla()
candidatura.definir_tabla()
candidatura_carrera.definir_tabla()
campus.definir_tabla()
edificio.definir_tabla()
aula.definir_tabla()
tipo_pago.definir_tabla()
departamento.definir_tabla()
profesor.definir_tabla()
nivel_academico.definir_tabla()
asignatura.definir_tabla()
plan_curricular.definir_tabla()
plazas.definir_tabla()
evento.definir_tabla()
profesor_asignatura.definir_tabla()
asignatura_plan.definir_tabla()
grupo.definir_tabla()
pago.definir_tabla()
examen.definir_tabla()

#####################################
# Teachers courses/subjects assignaments
#####################################

# db.define_table('teacher_course',
#     Field('teacher_id', 'reference teacher',
#         label=T('Teacher')
#     ),
#     Field('academic_year_id', 'reference academic_year',
#         label=T('Academic year')
#     ),
#     Field('ou_event_id', 'reference ou_event',
#         label=T("Event"),
#     ),
#     Field('student_group_id', 'reference student_group',
#         label=T("Group"),
#     ),
#     Field('status', 'boolean',
#         default=True,
#         label=T("Status"),
#     ),
# )

#####################################

## database initialization
from applications.agis.modules import tools

if not tools.probar_base_de_datos():
    # create default users groups
    tools.inicializar_administrador()
    tools.inicializar_base_datos()
    redirect(URL('default','index'))
