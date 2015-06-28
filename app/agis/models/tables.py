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

# ccf = db.Table(db, 'ccf',
#     Field('career1', 'reference career', label=T('Career'),),
#     Field('priority1','integer',default=0,label=T('Priority'),),
#     Field('career2', 'reference career', label=T('Career'),),
#     Field('priority2','integer',default=1,label=T('Priority'),),
# )
# ccf.career1.requires = IS_IN_DB(
#     db(db.career.career_des_id == db.career_des.id),
#     'career.id'
# )
# ccf.career2.requires = IS_IN_DB(
#     db(db.career.career_des_id == db.career_des.id),
#     'career.id',
# )

# # academic source
# db.define_table('academic_source',
#     Field('code','string',
#         length=1,
#         unique=True,
#         required=True,
#     ),
#     Field('name','string',
#         length=200,
#         required=True,
#     ),
#     format='%(name)s',
#     plural=T('Academic sources'),
#     singular=T('Academic source'),
# )
# db.academic_source.code.requires = [
#     IS_NOT_EMPTY(error_message=T('A code is required')),
#     IS_MATCH('^\d{1,1}$', error_message=T('Code is not valid')),
#     IS_NOT_IN_DB(db,'academic_source.code',
#         error_message=T('That academic source is alredy on database'),
#     )
# ]
# db.academic_source.name.requires = [
#     IS_NOT_EMPTY(error_message=T('A name is required')),
# ]

# # candidate with debt first stop to pass to student
# db.define_table('candidate_debt',
#     # laboral
#     Field('person', 'reference person',
#         unique=True,
#         label=T('Personal data'),
#         comment=T('Select or add personal data'),
#     ),
#     Field('is_worker','boolean',
#         default=False,
#         label=T('Is it working?'),
#     ),
#     Field('work_name','string',
#         required=False,
#         label=T('Job name'),
#     ),
#     Field('profession_name','string',
#         required=False,
#         label=T('Profession name'),
#     ),
#     # previos education
#     Field('educational_attainment','string',
#         length=5,
#         required=True,
#         notnull=True,
#         label=T('Educational attainment'),
#         comment=T('For example: 9th, 10th or 12th'),
#     ),
#     Field('previous_school', 'reference middle_school',
#         required=True,
#         label=T('Former school'),
#     ),
#     Field('previous_career', 'string',
#         length=50,
#         label=T('Name of the former career'),
#         required=True,
#         requires=IS_NOT_EMPTY(),
#     ),
#     Field('graduation_year','string',
#         length=4,
#         label=T('Graduation year'),
#         required=True,
#     ),
#     # institutional
#     Field('organic_unit', 'reference unidad_organica',
#         required=True,
#         label=T('Organic unit'),
#     ),
#     Field('special_education', 'list:reference special_education',
#         notnull=False,
#         required=False,
#         label=T('Special education needs'),
#         comment=T('Select zero or more'),
#     ),
#     Field('documents','list:integer',
#         required=False,
#         notnull=False,
#         label=T('Documents'),
#     ),
#     Field('regime', 'reference regime',
#         required=True,
#         label=T('Regime'),
#     ),
# )
# db.candidate_debt.regime.requires=IS_IN_DB(
#     db(db.regime.id == db.ou_regime.regime_id),
#     'regime.id',
#     '%(abbr)s|%(name)s',zero=None
# )
# db.candidate_debt.organic_unit.requires = IS_IN_DB(db,'unidad_organica.id',
#     '%(nombre)s',zero=None
# )
# db.candidate_debt.graduation_year.requires = [
#     IS_NOT_EMPTY(error_message=T('Please specify graduation year')),
#     IS_INT_IN_RANGE(1900, 2300, 
#         error_message=T('Must be between 1900 and 2299'),
#     )
# ]
# db.candidate_debt.previous_school.requires = IS_IN_DB(db, 'middle_school.id',
#     '%(name)s',zero=None
# )
# db.candidate_debt.person.requires = IS_IN_DB(db,'person.id',
#     '%(full_name)s',zero=None,
#     _and=IS_NOT_IN_DB(db,'candidate_debt.person'),
# )
# db.candidate_debt.work_name.length = 100
# db.candidate_debt.profession_name.length = 100
# db.candidate_debt.documents.requires = IS_IN_SET({
#     1: 'Certificado original',
#     2: 'Cópia de documento',
#     3: 'Documento de trabajo',
#     4: 'Documento Militar',
#     5: 'Internato',
# },zero=None, multiple=True)

# ## canditate - careers
# db.define_table('candidate_career',
#     Field('candidate', 'reference candidate_debt',
#         required=True,
#         label=T('Candidate'),
#     ),
#     Field('career', 'reference career',
#         required=True,
#         label=T('Career'),
#     ),
#     Field('priority','integer',
#         default=0,
#         label=T('Priority'),
#     ),
# )
# db.candidate_career.career.requires = IS_IN_DB(
#     db(db.career.career_des_id == db.career_des.id),
#     'career.id'
# )

# ## campus
# db.define_table('campus',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Name is required")),
#         label=T("Name"),
#     ),
#     Field('abbr', 'string',
#         length=10,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
#         label=T('Abbr'),
#     ),
#     Field('address','text',
#         label=T("Address"),
#     ),
#     Field('availability', 'boolean',
#         default=True,
#         label=T("Available?"),
#     ),
#     Field('organic_unit','reference unidad_organica',
#         label=T("Organic unit"),
#     ),
#     format="%(name)s",
# )
# db.campus.organic_unit.requires = IS_IN_DB(db,'unidad_organica.id',
#     '%(nombre)s',zero=None
# )

# ## buildings
# db.define_table('building',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Name is required")),
#         label=T("Name"),
#     ),
#     Field('abbr', 'string',
#         length=10,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
#         label=T('Abbr'),
#     ),
#     Field('availability', 'boolean',
#         default=True,
#         label=T("Available?"),
#     ),
#     Field('campus', 'reference campus'),
#     format="%(name)s",
# )
# db.building.campus.requires = IS_IN_DB(db, 'campus.id',
#     '%(name)s', zero=None
# )

# ## classroom
# db.define_table('classroom',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Name is required")),
#         label=T("Name"),
#     ),
#     Field('c_size', 'integer',
#         default=0,
#         required=False,
#         label=T("Size"),
#     ),
#     Field('availability', 'boolean',
#         default=True,
#         label=T("Available?"),
#     ),
#     Field('building', 'reference building',
#         label=T("Building"),),
#     format="%(name)s"
# )
# db.classroom.building.requires = IS_IN_DB(db, 'building.id',
#     '%(name)s', zero=None
# )


# ## payments
# PAYMENT_PERIODICITY = {1 : "Unique"}
# PAYMENT_TYPE = {
#     1: "Bank account",
#     2: "Credit card",
#     3: "Cash"
# }
# db.define_table('payment_concept',
#     Field('name','string',
#         label=T('Name'),
#         length=20,
#     ),
#     Field('periodicity', 'integer',
#         label=T('Periodicity'),
#         represent = lambda value,row: T(PAYMENT_PERIODICITY[value])
#     ),
#     Field('amount','double',
#         label=T('Amount'),
#         required=True,
#     ),
#     Field('status', 'boolean',
#         default=True,
#         required=True,
#         label=T('Status'),
#     ),
#     format="%(name)s",
# )
# db.payment_concept.id.label=T("Code")
# db.payment_concept.periodicity.requires = IS_IN_SET(PAYMENT_PERIODICITY,
#     zero=None
# )
# db.payment_concept.amount.requires.append(IS_NOT_EMPTY())
# db.payment_concept.name.requires = [IS_NOT_EMPTY(),
#     IS_NOT_IN_DB(db, 'payment_concept.name')
# ]
# db.define_table('payment',
#     Field('person', 'reference person',
#         label=T('Person'),
#     ),
#     Field('payment_concept', 'reference payment_concept',
#         label=T('Concept'),
#     ),
#     Field('payment_date', 'datetime',
#         label=T('Date & time'),
#     ),
#     Field('amount', 'double',
#         label=T('Amount'),
#     ),
#     Field('receipt_number', 'integer',
#         label=T('Receipt No.'),
#         comment=T('Receipt Number')
#     ),
# )
# db.define_table('payment_bank',
#     Field('payment', 'reference payment',
#         label=T('Payment'),
#     ),
#     Field('transaction_number', 'integer',
#         label=T('Transaction number'),
#     ),
# )
# db.define_table('payment_credit',
#     Field('payment', 'reference payment'),
# )
# db.define_table('payment_cash',
#     Field('payment', 'reference payment'),
# )
# db.payment.id.readable=False
# db.payment.id.writable=False
# db.payment.receipt_number.requires.append(IS_NOT_EMPTY())
# db.payment.person.widget = SQLFORM.widgets.autocomplete(
#     request, db.person.full_name,
#     id_field=db.person.id,
#     min_length=1,
# )
# db.payment_bank.transaction_number.requires.append(IS_NOT_EMPTY())
# db.payment.amount.requires.append(IS_NOT_EMPTY())
# db.payment.payment_date.requires = [IS_NOT_EMPTY(),
#     IS_DATETIME()
# ]
# db.payment.payment_concept.requires = IS_IN_DB(db, 'payment_concept.id',
#     '%(name)s', zero=None
# )
# db.payment.person.requires = IS_IN_DB(db,'person.id',
#     '%(full_name)s', zero=None
# )

# # acedemic level
# db.define_table('academic_level',
#     Field('name', 'string', label=T('Name'),
#         required=True,
#         notnull=True,
#     ),
#     format="%(name)s"
# )
# db.academic_level.id.label = T('ID')
# db.academic_level.name.requires = [IS_NOT_EMPTY(),
#     IS_NOT_IN_DB(db, 'academic_level.name'),
# ]

# # courses (subjects/materias)
# db.define_table('course',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=[IS_NOT_EMPTY(error_message=T("Name is required"))],
#         label=T("Name"),
#     ),
#     Field('abbr', 'string',
#         length=10,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
#         label=T('Abbr'),
#     ),
#     format='%(name)s',
# )
# db.course.name.requires.append(IS_NOT_IN_DB(db, 'course.name'))

# # student group
# db.define_table('student_group',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=[IS_NOT_EMPTY(error_message=T("Name is required"))],
#         label=T("Name"),
#     ),
#     Field('academic_year', 'reference academic_year',
#         label=T('Academic year'),
#     ),
#     Field('career_id', 'reference career',
#         label=T('Career'),
#     ),
#     Field('academic_level', 'reference academic_level',
#         label=T('Academic level'),
#     ),
#     Field('classroom', 'reference classroom',
#         label=T('Classroom'),
#     ),
#     Field('availability', 'boolean',
#         default=False,
#         label=T("Available?"),
#     ),
#     format="%(name)s",
# )
# db.student_group.name.requires.append(IS_NOT_IN_DB(db, 'student_group.name'))
# db.student_group.academic_year.requires = IS_IN_DB(db, 'academic_year.id',
#     '%(a_year)s', zero=None
# )
# db.student_group.academic_level.requires = IS_IN_DB(db, 'academic_level.id',
#     '%(name)s', zero=None
# )
# db.student_group.classroom.requires = IS_IN_DB(db, 'classroom.id',
#     '%(name)s', zero=None
# )

# # granted student access spaces
# db.define_table('gsa_spaces',
#     Field('academic_year', 'reference academic_year',
#         label=T('Academic year'),
#     ),
#     Field('career', 'reference career',
#         label=T('Career'),
#     ),
#     Field('regime', 'reference ou_regime',
#         label=T('Regime'),
#     ),
#     Field('amount', 'integer',
#         label=T('Amount'),
#         default=0,
#     ),
# )
# #db.gsa_spaces.academic_year.requires = IS_IN_DB(db, 'academic_year.id')


# def _academic_plan_format(r):
#     return "AP{0}{1}{2}".format(r.career_id, r.academic_level_id, r.course_id)
# db.define_table('academic_plan',
#     Field('career_id', 'reference career',
#         label=T('Career'),
#     ),
#     Field('academic_level_id', 'reference academic_level',
#         label=T('Academic level'),
#     ),
#     Field('course_id', 'reference course',
#         label=T('Course/Subject'),
#     ),
#     Field('status', 'boolean',
#         default=False,
#         label=T("Active ?"),
#     ),
#     format = _academic_plan_format
# )

# #department
# db.define_table('department',
#     Field('name','string',
#         length=100,
#         required=True,
#         requires=IS_NOT_EMPTY(error_message=T("Name is required")),
#         label=T("Name"),
#     ),
#     Field('organic_unit', 'reference organic_unit'),
#     format="%(name)s",
# )
# db.department.organic_unit.requires = IS_IN_DB(db, 'organic_unit.id',
#     '%(name)s', zero=None
# )

# # ou_event
# db.define_table('ou_event',
#     Field('name','string',
#         length=100,
#         required=True,
#         unique=True,
#         requires=IS_NOT_EMPTY(error_message=T("Name is required")),
#         label=T("Name"),
#     ),
#     Field('ou_event_type', 'integer',
#         required=True,
#         label=T('Event type'),
#     ),
#     Field('start_date', 'date',
#         required=True,
#         notnull=True,
#         label=T('Start date'),
#     ),
#     Field('end_date', 'date',
#         required=True,
#         notnull=True,
#         label=T('End date'),
#     ),
#     Field('academic_year', 'reference academic_year',
#         label=T('Academic Year'),),
#     Field('availability', 'boolean',
#         default=True,
#         label=T("Available?"),
#     ),
#     format="%(name)s"
# )
# db.ou_event.ou_event_type.requires = IS_IN_SET({
#     1: T('Enrollment'),
#     2: T('Registration'),
# }, zero=None)
# db.ou_event.academic_year.requires = IS_IN_DB(db, 'academic_year.id',
#     '%(a_year)s', zero=None
# )

######################################
# teachers
######################################
# TEACHER_BIND_VALS = (
#     ('0','Efectivo'),
#     ('1','Colaborador'),
#     ('2','Otros'),
# )
# TEACHER_CATEGORY_VALUES = (
#     ('0', 'Instructor'),
#     ('1', 'Asistente'),
#     ('2', 'Auxiliar'),
#     ('3', 'Asociado'),
#     ('4', 'Titular'),
#     ('5', 'Otros'),
# )
# TEACHER_DEGREE_VALUES = (
#     ('0', 'Bacharelato'),
#     ('1', 'Licenciatuara'),
#     ('2', 'Mestrado'),
#     ('3', 'Doutoramento'),
# )
# def _teacher_bind_represent(value, row):
#     return T(TEACHER_BIND_VALS[int(value)][1]) + " ({0})".format(value)
# def _teacher_category_represent(value, row):
#     return T(TEACHER_CATEGORY_VALUES[int(value)][1]) + " ({0})".format(value)
# def _teacher_degree_represent(value, row):
#     return T(TEACHER_DEGREE_VALUES[int(value)][1]) + " ({0})".format(value)
# def _teacher_format(row):
#     person = db.person[row.person_id]
#     return person.full_name
# db.define_table('teacher',
#     Field('person_id', 'reference person', label=T("Person")),
#     Field('teacher_bind', 'string', length=1, label=T("Bind"),
#         represent=_teacher_bind_represent,
#     ),
#     Field('teacher_category', 'string', length=1,label=T("Category"),
#         represent=_teacher_category_represent,
#     ),
#     Field('teacher_degree', 'string', length=1, label=T("Degree"),
#         represent=_teacher_degree_represent,
#     ),
#     # TODO: buscar palabra correcta en ingles
#     Field('date_of_entry', 'date',label=T("Since")),
#     Field('department_id', 'reference department',label=T("Department")),
#     Field('status', 'boolean',
#         default=True,
#         label=T("Status"),
#     ),
#     format=_teacher_format,
# )
# db.teacher.department_id.requires = IS_IN_DB(db, 'department.id', "%(name)s",
#     zero=None,
# )
# db.teacher.date_of_entry.requires.append(IS_NOT_EMPTY(
#     error_message=T("Date of entry is required"),
# ))
# db.teacher.teacher_bind.requires=IS_IN_SET(TEACHER_BIND_VALS,zero=None,)
# db.teacher.teacher_category.requires=IS_IN_SET(
#     TEACHER_CATEGORY_VALUES,zero=None,
# )
# db.teacher.teacher_degree.requires=IS_IN_SET(TEACHER_DEGREE_VALUES,zero=None,)
######################################

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
