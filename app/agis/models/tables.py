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
#
# TODO: Depués de migrar todas las tablas a este formato comentar
#       esto y en cada vista solo llamar las tablas necesarias.
#
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

# # careers
# def career_format(r):
#     career_des = db.career_des[r.career_des_id]
#     return career_des.name
# db.define_table('career',
#     Field('career_des_id', 'reference career_des',
#         label=T('Career Description'),
#     ),
#     Field('organic_unit_id', 'reference unidad_organica',
#         label=T('Organic Unit'),
#     ),
#     format=career_format,
# )
# db.career.organic_unit_id.requires = IS_IN_DB(db,
#     'unidad_organica.id', '%(nombre)s', zero=None,
# )
# db.career.career_des_id.requires = IS_IN_DB(
#     db,
#     'career_des.id', '%(name)s', zero=None,
# )
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


# # OU regimes
# def _ou_regime_format(r):
#     regime = db.regime[r.regime_id]
#     return regime.name
# db.define_table('ou_regime',
#     Field('regime_id', 'reference regime',
#         label=T('Regime description'),
#         required=True,
#         notnull=True,
#     ),
#     Field('organic_unit_id', 'reference unidad_organica',
#         label=T('Organic Unit'),
#         required=True,
#         notnull=True,
#     ),
#     singular=T('Regime'),
#     plural=T('Regimes'),
#     format=_ou_regime_format
# )
# db.ou_regime.organic_unit_id.requires = IS_IN_DB(db,'unidad_organica.id',
#     '%(nombre)s',
#     zero=None,
#     error_message=T('Choose one organic unit'),
# )

# # academic year
# db.define_table('academic_year',
#     Field('a_year', 'integer',
#         required=True,
#         notnull=True,
#         unique=True,
#         label=T('Year'),
#         comment=T('In the format YYYY'),
#     ),
#     Field('description', 'string',
#         length=200,
#         label=T('Description'),
#     ),
#     singular=T('Academic year'),
#     plural=T('Academic years'),
#     format='%(a_year)d',
# )
# db.academic_year.a_year.requires = [
#     IS_NOT_EMPTY(error_message=T('Please specify the year')),
#     IS_INT_IN_RANGE(1970, 2300, 
#         error_message=T('Must be between 1970 and 2299'),
#     ),
#     IS_NOT_IN_DB(db,'academic_year.a_year',
#         error_message=T('This academic year is already in the database'),
#     ),
# ]



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

# #special education needs
# db.define_table('special_education',
#     Field('code','string',
#         length=1,
#         unique=True,
#         required=True,
#         label=T('Code'),
#     ),
#     Field('name','string',
#         length=200,
#         required=True,
#         label=T('Name'),
#     ),
#     format='%(name)s',
#     plural=T('Special education needs'),
#     singular=T('Special education need'),
# )
# db.special_education.code.requires = [
#     IS_NOT_EMPTY(error_message=T('A code is required')),
#     IS_MATCH('^\d{1,1}$', error_message=T('Code is not valid')),
#     IS_NOT_IN_DB(db,'special_education.code',
#         error_message=T('That special education need is alredy on database'),
#     )
# ]
# db.special_education.name.requires = [
#     IS_NOT_EMPTY(error_message=T('A name is required')),
# ]

# # Identity Card Types
# db.define_table('identity_card_type',
#     Field('name', 'string',
#         length=70,
#         required=True,
#         notnull=True,
#         label=T('Name'),
#     ),
#     format='%(name)s',
# )
# db.identity_card_type.name.requires = [
#     IS_NOT_EMPTY(error_message=T('A name is required')),
#     IS_NOT_IN_DB(db, 'identity_card_type.name',
#         error_message=T('That identity card type is alredy on database'),
#     ),
# ]

# # Middle school types
# db.define_table('middle_school_type',
#     Field('code','string',length=2,
#         label=T('Code'),
#         notnull=True,
#         required=True,
#         unique=True,
#         comment=T('Two-digit code'),
#     ),
#     Field('name','string',length=10,
#         label=T('Name'),
#         required=True,
#         notnull=True,
#     ),
#     format='%(name)s',
# )
# db.middle_school_type.code.requires = [
#     IS_NOT_EMPTY(error_message=T('A code is required')),
#     IS_MATCH('^\d{2,2}$', error_message=T('Code is not valid')),
#     IS_NOT_IN_DB(db,'middle_school_type.code',
#         error_message=T('That school type is alredy on database'),
#     )
# ]
# db.middle_school_type.name.requires = [
#     IS_NOT_EMPTY(error_message=T('A name is required')),
#     IS_NOT_IN_DB(db, 'middle_school_type.name',
#         error_message=T('That school type  is alredy on database'),
#     ),
# ]


# # Person
# db.define_table('person',
#     # personal data
#     Field('name','string',
#         required=True,
#         length=20,
#         notnull=True,
#         label=T('First name'),
#     ),
#     Field('first_name','string',
#         required=True,
#         length=20,
#         label=T('Second name'),
#     ),
#     Field('last_name','string',
#         required=True,
#         length=20,
#         notnull=True,
#         label=T('Last name'),
#     ),
#     Field('date_of_birth', 'date',
#         required=True,
#         notnull=True,
#         label=T('Birth date'),
#     ),
#     Field('place_of_birth', 'reference commune',
#         label=T('Birth place'),
#     ),
#     Field('gender', 'integer',
#         required=True,
#         label=T('Gender'),
#     ),
#     Field('marital_status', 'integer',
#         required=True,
#         label=T('Marital Status'),
#     ),
#     Field('identity_type', 'reference identity_card_type',
#         label=T('Identity type'),
#     ),
#     Field('identity_number', 'string',
#         length=50,
#         required=True,
#         notnull=True,
#         label=T('Identity number'),
#     ),
#     Field('father_name','string',
#         length=50,
#         required=True,
#         notnull=True,
#         label=T('Father name'),
#     ),
#     Field('mother_name','string',
#         length=50,
#         required=True,
#         notnull=True,
#         label=T('Mother name'),
#     ),
#     Field('nationality', 'string',
#         length=50,
#         required=True,
#         notnull=True,
#         label=T('Nationality'),
#     ),
#     Field('political_status', 'integer',
#         required=True,
#         label=T('Status'),
#     ),
#     Field('full_name',
#         compute=lambda r: "{0} {1} {2}".format(r.name,r.first_name,r.last_name),
#         label=T('Full Name')
#     ),
#     #contact data
#     Field('municipality', 'reference municipality',
#         label=T('Municipality'),
#     ),
#     Field('commune', 'reference commune',
#           label=T('Commune'),
#     ),
#     Field('address','text',
#           label=T('Address'),
#     ),
#     Field('phone_number','string',
#           label=T('Phone Number'),
#     ),
#     Field('email', 'string',
#           label=T('Email'),
#     ),
#     Field('sys_status','boolean',
#         default=True,
#         notnull=True,
#         writable=False,
#         readable=False,
#     ),
#     format='%(full_name)s'
# )
# db.person.commune.requires = IS_IN_DB(db,'commune.id',
#     '%(name)s',
#     zero=None,
#     error_message=T('Commune is required'),
# )
# db.person.municipality.requires = IS_IN_DB(db,'municipality.id',
#     '%(name)s',
#     zero=None,
#     error_message=T('Municipality is required'),
# )
# db.person.place_of_birth.requires = IS_IN_DB(db,'commune.id',
#     '%(name)s',
#     zero=None,
#     error_message=T('Birth place is required'),
# )

# db.person.identity_type.requires = IS_IN_DB(db,'identity_card_type.id',
#     '%(name)s',
#     zero=None,
#     error_message=T('Identity type is required'),
# )
# db.person.political_status.requires = IS_IN_SET({
#     1: T('Civil'),
#     2: T('Military'),
#     3: T('Police'),
# }, zero=None)
# db.person.gender.requires = IS_IN_SET({
#     1: T('Male'),
#     2: T('Female'),
# }, zero=None)
# db.person.marital_status.requires = IS_IN_SET({
#     1: T('Single'),
#     2: T('Married'),
#     3: T('Divorcee'),
#     4: T('Other'),
# }, zero=None)

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
