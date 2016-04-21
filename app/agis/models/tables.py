# -*- coding: utf-8 -*-
'''
Created on 18/5/2015

@author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
'''
from agiscore.db import region_academica
from agiscore.db import provincia
from agiscore.db import municipio
from agiscore.db import comuna
from agiscore.db import escuela
from agiscore.db import unidad_organica
from agiscore.db import descripcion_carrera
from agiscore.db import regimen
from agiscore.db import tipos_ensennanza
from agiscore.db import escuela_media
from agiscore.db import tipo_documento_identidad
from agiscore.db import discapacidad
from agiscore.db import regimen_uo
from agiscore.db import carrera_uo
from agiscore.db import persona
from agiscore.db import estudiante
from agiscore.db import candidatura
from agiscore.db import ano_academico
from agiscore.db import candidatura_carrera
from agiscore.db import campus
from agiscore.db import edificio
from agiscore.db import aula
from agiscore.db import tipo_pago
from agiscore.db import departamento
from agiscore.db import profesor
from agiscore.db import nivel_academico
from agiscore.db import asignatura
from agiscore.db import plan_curricular
from agiscore.db import plazas
from agiscore.db import evento
from agiscore.db import profesor_asignatura
from agiscore.db import asignatura_plan
from agiscore.db import grupo
from agiscore.db import pago
from agiscore.db import examen
from agiscore.db import examen_aula_estudiante
from agiscore.db import nota
from agiscore.db import asignacion_carrera
from agiscore.db import pais
from agiscore.db import carrera_escuela
from agiscore.db import funsionario
from agiscore.db import especialidad
from agiscore.db import turma
from agiscore.db import matricula
from agiscore.db import pago_propina
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
funsionario.definir_tabla(db, T)
nivel_academico.definir_tabla()
asignatura.definir_tabla()
plan_curricular.definir_tabla()
plazas.definir_tabla()
evento.definir_tabla()
profesor_asignatura.definir_tabla()
asignatura_plan.definir_tabla()
grupo.definir_tabla()
pago.definir_tabla(db, T)
examen.definir_tabla()
examen_aula_estudiante.definir_tabla()
nota.definir_tabla()
asignacion_carrera.definir_tabla()
pais.definir_tabla()
carrera_escuela.definir_tabla(db, T)
especialidad.definir_tabla(db, T)
turma.definir_tabla(db, T)
matricula.definir_tabla(db, T)
pago_propina.definir_tabla(db, T)

# configurar otras
db.auth_user.id.readable = False

## database initialization
from agiscore import tools

if not tools.probar_base_de_datos():
    # create default users groups
    tools.inicializar_seguridad()
    tools.inicializar_base_datos()
    redirect(URL('default','index'))

auth.enable_record_versioning(db)
