# -*- coding: utf-8 -*-
'''
Created on 18/5/2015

@author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
'''

db.define_table('academic_region',
    Field('name', 'string',
        length=50,
        required=True,
        notnull=True,
        label=T('Region name'),
    ),
    Field('code','string',
        length=2,
        required=True,
        notnull=True,
        unique=True,
        label=T('Code'),
        comment=T('Two-digit code'),
    ),
    format='%(name)s - %(code)s',
    singular=T('Academic region'),
    plural=T('Academic regions'),
)
db.academic_region.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
    IS_NOT_IN_DB(db,'academic_region.name',
        error_message=T('An academic region already exists with that name'),
    ),
]
db.academic_region.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_MATCH('^\d{2,2}$', error_message = T('Invalid code')),
    IS_NOT_IN_DB(db,'academic_region.code',
        error_message=T('An academic region alredy exists with that code'),
    ),
]


# province
db.define_table('province',
    Field('code','string',
        length=2,
        unique=True,
        required=True,
        label=T('Code'),
        comment=T("Two-digit code"),
    ),
    Field('name','string',
        length=50,
        required=True,
        notnull=True,
        label=T('Name'),
    ),
    Field('ar_id', 'reference academic_region',
        ondelete='SET NULL',
        label=T('Academic region'),
    ),
    format='%(name)s',
    singular=T('Province'),
    plural=T('Provinces'),
)
db.province.code.requires = [
    IS_NOT_EMPTY(error_message=T('Code is required')),
    IS_NOT_IN_DB(db, 'province.code',
        error_message=T('Province code already in the database')
    ),
]
db.province.name.requires = [
    IS_NOT_EMPTY(error_message=T('Province name is required')),
    IS_NOT_IN_DB(db, 'province.name',
        error_message=T('Province already in the database'),
    ),
]
db.province.ar_id.requires = IS_IN_DB(db, 'academic_region.id',
    '%(code)s - %(name)s',
    zero=None,
)

#Institutes of Higher Education IHE
def __comp_IHE_code(r):
    ar = db.academic_region[r['ar_id']]
    return ar.code + r['classification'] + r['nature'] + r['registration_code']
db.define_table('IHE',
    Field('name', 'string',
        length=100,
        required=True,
        label=T('Name'),
    ),
    Field('ar_id', 'reference academic_region',
        ondelete='SET NULL',
        label=T('Academic region'),
    ),
    Field('classification','string',
        length=2,
        required=True,
        label=T('Classification'),
    ),
    Field('nature','string',
        length=1,
        required=True,
        label=T('Nature'),
    ),
    Field('registration_code','string',
        length=3,
        required=True,
        label=T('Registration Code'),
        comment=T(
            '''Registration code in Ministry.
            Should be 3 consecutive digits, for example 001
            '''
        )
    ),
    Field('code',
        compute=__comp_IHE_code,
        notnull=True,
        label=T('Code'),
    ),
    Field('logo','upload',
        required=False,
        notnull=False,
        autodelete=True,
        uploadseparate=True,
        label=T('Logo'),
    ),
    format='%(name)s',
    singular=T('Institute of Higher Education'),
    plural=T('Institutes of Higher Education'),
)
db.IHE.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
    IS_NOT_IN_DB(db,'IHE.name',
        error_message=T('IHE name is already in the database'),
    )
]
db.IHE.ar_id.requires = IS_IN_DB(db,'academic_region.id',
    '%(code)s - %(name)s',
    zero=T('Choose one:'),
    error_message=T('Choose one academic region'),
)
db.IHE.logo.requires = IS_EMPTY_OR(IS_IMAGE())
db.IHE.classification.requires = IS_IN_SET({
    '10': T('University'),
    '20': T('Higher Institute'),
    '21': T('Higher Polytechnic Institute'),
    '30': T('Higher School'),
    '31': T('Higher Technical School'),
    '32': T('Higher Polytechnic School'),
    '40': T('Academy'),
    '70': T('Scientific Research Center'),
},zero=None)
db.IHE.nature.requires = IS_IN_SET({
    '1': T('Public'),
    '2': T('Private'),
    '3': T('Public & Private'),
},zero=None)
db.IHE.registration_code.requires = [
    IS_NOT_EMPTY(error_message=T('Registration code is required')),
    IS_MATCH('^\d{3,3}$', error_message=T('Wrong registration code')),
    IS_NOT_IN_DB(db,'IHE.registration_code'),
]

#organic units
def __comp_ou_code(r):
    ihe = db.IHE[r['IHE_id']]
    return (ihe.code +
        r['aggregation_level'] +
        r['classification'] +
        r['registration_code']
    )
db.define_table('organic_unit',
    Field('code',
        compute=__comp_ou_code,
        notnull=True,
        label=T('Code'),
    ),
    Field('name','string',
        required=True,
        notnull=True,
        length=100,
        label=T('Name'),
    ),
    Field('address', 'text',
        required=False,
        notnull=False,
        label=T('Address'),
    ),
    Field('province_id', 'reference province',
        ondelete="SET NULL",
        label=T('Province')
    ),
    Field('aggregation_level', 'string',
        required=True,
        label=T('Aggregation level'),
        length=1,
    ),
    Field('classification','string',
        length=2,
        required=True,
        label=T('Classification'),
    ),
    Field('registration_code','string',
        length=3,
        required=True,
        label=T('Registration Code'),
        comment=T(
            '''Registration code in Ministry.
            Should be 3 consecutive digits, for example 001
            '''
        )
    ),
    Field('IHE_asigg_code', 'string',
        length=2,
        label=T('Code Assigned by the IHS'),
        required=True,
        notnull=True,
        comment=T(
            '''Registration code by the IHS.
            Should be 2 consecutive digits, for example 01
            '''
        )
    ),
    Field('IHE_id', 'reference IHE',
        ondelete='SET NULL',
        label=T('Institutes of Higher Education'),
        required=True,
    ),
    format='%(name)s',
    singular=T('Organic Unit'),
    plural=T('Organic Units'),
)
db.organic_unit.aggregation_level.requires = IS_IN_SET({
    '1': T('Headquarters'),
    '2': T('Organic Unit'),
},zero=None)
db.organic_unit.classification.requires = IS_IN_SET({
    '20': T('Higher institute'),
    '21': T('Higher Technical Institute'),
    '22': T('Polytechnic Institute'),
    '30': T('Higher School'),
    '31': T('Higher Technical School'),
    '32': T('Higher Polytechnic School'),
    '40': T('Academy'),
    '50': T('Faculty'),
    '60': T('Department'),
    '70': T('Scientific Research Center'),
},zero=None)
db.organic_unit.registration_code.requires = [
    IS_NOT_EMPTY(error_message=T('Registration code is required')),
    IS_MATCH('^\d{3,3}$', error_message=T('Invalid registration code')),
    IS_NOT_IN_DB(db,'organic_unit.registration_code'),
]
db.organic_unit.IHE_asigg_code.requires = [
    IS_NOT_EMPTY(error_message=T('Valid code is required')),
    IS_MATCH('^\d{2,2}$', error_message=T('Invalid registration code')),
    IS_NOT_IN_DB(db,'organic_unit.IHE_asigg_code',
        error_message=T('Registration code is alredy in database'),
    ),
]
db.organic_unit.name.requires = IS_NOT_EMPTY(
    error_message=T('A name is required'),
)
db.organic_unit.province_id.requires = IS_IN_DB(db, 'province.id',
    '%(name)s',
    zero=T('Choose one'),
    error_message=T('Choose one province'),
)
db.organic_unit.IHE_id.requires = IS_IN_DB(db, 'IHE.id',
    '%(name)s',
    zero=T('Choose one'),
    error_message=T('Choose one IHE'),
)

## career descriptions
def __comp_career_des_code(r):
    return r['cod_mes'] + r['cod_pnfq'] + r['cod_unesco'] + r['cod_career']
db.define_table('career_des',
    Field('name','string',
        length=100,label=T('Name'),notnull=True,required=True
    ),
    Field('cod_mes', 'string',
        length=1,label='MES',notnull=True,required=True,
        comment=T('One digit code'),
    ),
    Field('cod_pnfq', 'string',
        length=2,label='PNFQ',notnull=True,required=True,
        comment=T('Two-digit code')
    ),
    Field('cod_unesco', 'string',
        length=3,label='UNESCO',notnull=True,required=True,
        comment=T('Three-digit code')
    ),
    Field('cod_career', 'string',
        length=3,label=T('Career code'),notnull=True,required=True,
        comment=T('Three-digit code')
    ),
    Field('code', 'string',
        length=9,label=T('Code'), compute=__comp_career_des_code,
        notnull=True,required=False,unique=True
    ),
    format='%(name)s',
    singular=T('Career Description'),
    plural=T('Career Descriptions'),
)
db.career_des.cod_mes.requires = [
    IS_NOT_EMPTY(),
    IS_MATCH('^\d{1,1}$', error_message=T('Malformed MES code')),
]
db.career_des.cod_pnfq.requires = [
    IS_NOT_EMPTY(),
    IS_MATCH('^\d{2,2}$', error_message=T('Malformed PNFQ code')),
]
db.career_des.name.requires = [
    IS_NOT_EMPTY(error_message=T('Career name is required')),
    IS_NOT_IN_DB(db,'career_des.name')
]
db.career_des.cod_unesco.requires = [
    IS_NOT_EMPTY(),
    IS_MATCH('^\d{3,3}$', error_message=T('Malformed UNESCO code')),
]
db.career_des.cod_career.requires = [
    IS_NOT_EMPTY(),
    IS_MATCH('^\d{3,3}$', error_message=T('Malformed career code')),
]

# careers
def career_format(r):
    career_des = db.career_des[r.career_des_id]
    return career_des.name
db.define_table('career',
    Field('career_des_id', 'reference career_des',
        label=T('Career Description'),
    ),
    Field('organic_unit_id', 'reference organic_unit',
        label=T('Organic Unit'),
    ),
    format=career_format,
)
db.career.organic_unit_id.requires = IS_IN_DB(db,
    'organic_unit.id', '%(name)s', zero=None,
)
db.career.career_des_id.requires = IS_IN_DB(
    db,
    'career_des.id', '%(name)s', zero=None,
)
ccf = db.Table(db, 'ccf',
    Field('career1', 'reference career', label=T('Career'),),
    Field('priority1','integer',default=0,label=T('Priority'),),
    Field('career2', 'reference career', label=T('Career'),),
    Field('priority2','integer',default=1,label=T('Priority'),),
)
ccf.career1.requires = IS_IN_DB(
    db(db.career.career_des_id == db.career_des.id),
    'career.id'
)
ccf.career2.requires = IS_IN_DB(
    db(db.career.career_des_id == db.career_des.id),
    'career.id',
)

# regime
db.define_table('regime',
    Field('code', 'string',
        length=1,
        required=True,
        label=T('Code'),
        unique=True,
    ),
    Field('name', 'string',
        length=50,
        required=True,
        label=T('Name'),
    ),
    Field('abbr', 'string',
        length=1,
        required=True,
        requires=IS_NOT_EMPTY(),
        label=T('Abbreviation'),
    ),
    format='%(name)s',
    singular=T('Regime'),
    plural=T('Regimes'),
)
db.regime.code.requires = [
    IS_NOT_EMPTY(error_message=T('Code name is required')),
    IS_NOT_IN_DB(db, 'regime.code',
        error_message=T('Code already in the database'),
    )
]
db.regime.name.requires = [
    IS_NOT_EMPTY(error_message=T('Regime name is required')),
    IS_NOT_IN_DB(db, 'regime.name',
        error_message=T('Regime already in the database'),
    )
]
db.regime.abbr.requires = IS_NOT_EMPTY(
    error_message=T('Abbreviation of name is required')
)

# OU regimes
def _ou_regime_format(r):
    regime = db.regime[r.regime_id]
    return regime.name
db.define_table('ou_regime',
    Field('regime_id', 'reference regime',
        label=T('Regime description'),
        required=True,
        notnull=True,
    ),
    Field('organic_unit_id', 'reference organic_unit',
        label=T('Organic Unit'),
        required=True,
        notnull=True,
    ),
    singular=T('Regime'),
    plural=T('Regimes'),
    format=_ou_regime_format
)
db.ou_regime.organic_unit_id.requires = IS_IN_DB(db,'organic_unit.id',
    '%(name)s',
    zero=None,
    error_message=T('Choose one organic unit'),
)

# academic year
db.define_table('academic_year',
    Field('a_year', 'integer',
        required=True,
        notnull=True,
        unique=True,
        label=T('Year'),
        comment=T('In the format YYYY'),
    ),
    Field('description', 'string',
        length=200,
        label=T('Description'),
    ),
    singular=T('Academic year'),
    plural=T('Academic years'),
    format='%(a_year)d',
)
db.academic_year.a_year.requires = [
    IS_NOT_EMPTY(error_message=T('Please specify the year')),
    IS_INT_IN_RANGE(1970, 2300, 
        error_message=T('Must be between 1970 and 2299'),
    ),
    IS_NOT_IN_DB(db,'academic_year.a_year',
        error_message=T('This academic year is already in the database'),
    ),
]


# Municipality
db.define_table('municipality',
    Field('code', 'string',
        length=2,
        required=True,
        notnull=True,
        label=T('Code'),
        comment=T('Two digit code'),
    ),
    Field('name', 'string',
        length=80,
        required=True,
        unique=True,
        notnull=True,
        label=T('Name'),
    ),
    Field('province', 'reference province'),
    plural=T('Municipalities'),
    singular=T('Municipality'),
    format='%(name)s',
)
db.municipality.code.requires = [
    IS_NOT_EMPTY(error_message=T('Municipality code is required')),
    IS_MATCH('^\d\d$', error_message=T('Code is not valid')),
]
db.municipality.name.requires = [
    IS_NOT_EMPTY(error_message=T('Municipality name is required')),
    IS_NOT_IN_DB(db, 'municipality.name'),
]
db.municipality.province.requires = IS_IN_DB(db,'province.id',
    '%(name)s',
    #zero=T('Choose one') + ':',
    zero=None,
)


# Commune
db.define_table('commune',
    Field('code','string',
        length=2,
        label=T('Code'),
        required=True,
        notnull=True,
    ),
    Field('name','string',
        length=100,
        label=T('Name'),
        required=True,
        notnull=True,
    ),
    Field('municipality', 'reference municipality',
        required=True,
        label=T('Municipality'),
    ),
    format='%(name)s - %(municipality)s',
    plural=T('Communes'),
    singular=T('Commune'),
)
db.commune.code.requires = [
    IS_NOT_EMPTY(error_message=T('Commune code is required')),
    IS_MATCH('^\d\d$', error_message=T('Code is not valid')),
]
db.commune.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
]
db.commune.municipality.requires = IS_IN_DB(db,'municipality.id',
    '%(name)s',
    zero=None,
    error_message=T('A municipality is required'),
)


# academic source
db.define_table('academic_source',
    Field('code','string',
        length=1,
        unique=True,
        required=True,
    ),
    Field('name','string',
        length=200,
        required=True,
    ),
    format='%(name)s',
    plural=T('Academic sources'),
    singular=T('Academic source'),
)
db.academic_source.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_MATCH('^\d{1,1}$', error_message=T('Code is not valid')),
    IS_NOT_IN_DB(db,'academic_source.code',
        error_message=T('That academic source is alredy on database'),
    )
]
db.academic_source.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
]

#special education needs
db.define_table('special_education',
    Field('code','string',
        length=1,
        unique=True,
        required=True,
        label=T('Code'),
    ),
    Field('name','string',
        length=200,
        required=True,
        label=T('Name'),
    ),
    format='%(name)s',
    plural=T('Special education needs'),
    singular=T('Special education need'),
)
db.special_education.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_MATCH('^\d{1,1}$', error_message=T('Code is not valid')),
    IS_NOT_IN_DB(db,'special_education.code',
        error_message=T('That special education need is alredy on database'),
    )
]
db.special_education.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
]

# Identity Card Types
db.define_table('identity_card_type',
    Field('name', 'string',
        length=70,
        required=True,
        notnull=True,
        label=T('Name'),
    ),
    format='%(name)s',
)
db.identity_card_type.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
    IS_NOT_IN_DB(db, 'identity_card_type.name',
        error_message=T('That identity card type is alredy on database'),
    ),
]

# Middle school types
db.define_table('middle_school_type',
    Field('code','string',length=2,
        label=T('Code'),
        notnull=True,
        required=True,
        unique=True,
        comment=T('Two-digit code'),
    ),
    Field('name','string',length=10,
        label=T('Name'),
        required=True,
        notnull=True,
    ),
    format='%(name)s',
)
db.middle_school_type.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_MATCH('^\d{2,2}$', error_message=T('Code is not valid')),
    IS_NOT_IN_DB(db,'middle_school_type.code',
        error_message=T('That school type is alredy on database'),
    )
]
db.middle_school_type.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
    IS_NOT_IN_DB(db, 'middle_school_type.name',
        error_message=T('That school type  is alredy on database'),
    ),
]

# Middle schools
db.define_table('middle_school',
    Field('code', 'string',length=4,
        label=T('Code'),
        required=True,
        notnull=True,
        comment=T("Four-digit code"),
    ),
    Field('name', 'string',length=100,
        label=T('Name'),
        required=True,
        notnull=True,
    ),
    Field('province', 'reference province'),
    Field('municipality', 'reference municipality'),
    Field('school_type', 'reference middle_school_type'),
)
db.middle_school.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_MATCH('^\d{4,4}$', error_message=T('Code is not valid')),
    IS_NOT_IN_DB(db,'middle_school.code',
        error_message=T('That school is alredy on database'),
    )
]
db.middle_school.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
    IS_NOT_IN_DB(db, 'middle_school.name',
        error_message=T('That school is alredy on database'),
    ),
]
db.middle_school.school_type.requires = IS_IN_DB(db,'middle_school_type.id',
    '%(name)s',
    zero=None,
    error_message=T('School type is required'),
)


# Person
db.define_table('person',
    # personal data
    Field('name','string',
        required=True,
        length=20,
        notnull=True,
        label=T('First name'),
    ),
    Field('first_name','string',
        required=True,
        length=20,
        label=T('Second name'),
    ),
    Field('last_name','string',
        required=True,
        length=20,
        notnull=True,
        label=T('Last name'),
    ),
    Field('date_of_birth', 'date',
        required=True,
        notnull=True,
        label=T('Birth date'),
    ),
    Field('place_of_birth', 'reference commune',
        label=T('Birth place'),
    ),
    Field('gender', 'integer',
        required=True,
        label=T('Gender'),
    ),
    Field('marital_status', 'integer',
        required=True,
        label=T('Marital Status'),
    ),
    Field('identity_type', 'reference identity_card_type',
        label=T('Identity type'),
    ),
    Field('identity_number', 'string',
        length=50,
        required=True,
        notnull=True,
        label=T('Identity number'),
    ),
    Field('father_name','string',
        length=50,
        required=True,
        notnull=True,
        label=T('Father name'),
    ),
    Field('mother_name','string',
        length=50,
        required=True,
        notnull=True,
        label=T('Mother name'),
    ),
    Field('nationality', 'string',
        length=50,
        required=True,
        notnull=True,
        label=T('Nationality'),
    ),
    Field('political_status', 'integer',
        required=True,
        label=T('Status'),
    ),
    Field('full_name',
        compute=lambda r: "{0} {1} {2}".format(r.name,r.first_name,r.last_name),
        label=T('Full Name')
    ),
    #contact data
    Field('municipality', 'reference municipality',
        label=T('Municipality'),
    ),
    Field('commune', 'reference commune',
          label=T('Commune'),
    ),
    Field('address','text',
          label=T('Address'),
    ),
    Field('phone_number','string',
          label=T('Phone Number'),
    ),
    Field('email', 'string',
          label=T('Email'),
    ),
    Field('sys_status','boolean',
        default=True,
        notnull=True,
        writable=False,
        readable=False,
    ),
    format='%(full_name)s'
)
db.person.commune.requires = IS_IN_DB(db,'commune.id',
    '%(name)s',
    zero=None,
    error_message=T('Commune is required'),
)
db.person.municipality.requires = IS_IN_DB(db,'municipality.id',
    '%(name)s',
    zero=None,
    error_message=T('Municipality is required'),
)
db.person.place_of_birth.requires = IS_IN_DB(db,'commune.id',
    '%(name)s',
    zero=None,
    error_message=T('Birth place is required'),
)

db.person.identity_type.requires = IS_IN_DB(db,'identity_card_type.id',
    '%(name)s',
    zero=None,
    error_message=T('Identity type is required'),
)
db.person.political_status.requires = IS_IN_SET({
    1: T('Civil'),
    2: T('Military'),
    3: T('Police'),
}, zero=None)
db.person.gender.requires = IS_IN_SET({
    1: T('Male'),
    2: T('Female'),
}, zero=None)
db.person.marital_status.requires = IS_IN_SET({
    1: T('Single'),
    2: T('Married'),
    3: T('Divorcee'),
    4: T('Other'),
}, zero=None)

# candidate with debt first stop to pass to student
db.define_table('candidate_debt',
    # laboral
    Field('person', 'reference person',
        unique=True,
        label=T('Personal data'),
        comment=T('Select or add personal data'),
    ),
    Field('is_worker','boolean',
        default=False,
        label=T('Is it working?'),
    ),
    Field('work_name','string',
        required=False,
        label=T('Job name'),
    ),
    Field('profession_name','string',
        required=False,
        label=T('Profession name'),
    ),
    # previos education
    Field('educational_attainment','string',
        length=5,
        required=True,
        notnull=True,
        label=T('Educational attainment'),
        comment=T('For example: 9th, 10th or 12th'),
    ),
    Field('previous_school', 'reference middle_school',
        required=True,
        label=T('Former school'),
    ),
    Field('previous_career', 'string',
        length=50,
        label=T('Name of the former career'),
        required=True,
        requires=IS_NOT_EMPTY(),
    ),
    Field('graduation_year','string',
        length=4,
        label=T('Graduation year'),
        required=True,
    ),
    # institutional
    Field('organic_unit', 'reference organic_unit',
        required=True,
        label=T('Organic unit'),
    ),
    Field('special_education', 'list:reference special_education',
        notnull=False,
        required=False,
        label=T('Special education needs'),
        comment=T('Select zero or more'),
    ),
    Field('documents','list:integer',
        required=False,
        notnull=False,
        label=T('Documents'),
    ),
    Field('regime', 'reference regime',
        required=True,
        label=T('Regime'),
    ),
)
db.candidate_debt.regime.requires=IS_IN_DB(
    db(db.regime.id == db.ou_regime.regime_id),
    'regime.id',
    '%(abbr)s|%(name)s',zero=None
)
db.candidate_debt.organic_unit.requires = IS_IN_DB(db,'organic_unit.id',
    '%(name)s',zero=None
)
db.candidate_debt.graduation_year.requires = [
    IS_NOT_EMPTY(error_message=T('Please specify graduation year')),
    IS_INT_IN_RANGE(1900, 2300, 
        error_message=T('Must be between 1900 and 2299'),
    )
]
db.candidate_debt.previous_school.requires = IS_IN_DB(db, 'middle_school.id',
    '%(name)s',zero=None
)
db.candidate_debt.person.requires = IS_IN_DB(db,'person.id',
    '%(full_name)s',zero=None,
    _and=IS_NOT_IN_DB(db,'candidate_debt.person'),
)
db.candidate_debt.work_name.length = 100
db.candidate_debt.profession_name.length = 100
db.candidate_debt.documents.requires = IS_IN_SET({
    1: 'Certificado original',
    2: 'Cópia de documento',
    3: 'Documento de trabajo',
    4: 'Documento Militar',
    5: 'Internato',
},zero=None, multiple=True)

## canditate - careers
db.define_table('candidate_career',
    Field('candidate', 'reference candidate_debt',
        required=True,
        label=T('Candidate'),
    ),
    Field('career', 'reference career',
        required=True,
        label=T('Career'),
    ),
    Field('priority','integer',
        default=0,
        label=T('Priority'),
    ),
)
db.candidate_career.career.requires = IS_IN_DB(
    db(db.career.career_des_id == db.career_des.id),
    'career.id'
)

## campus
db.define_table('campus',
    Field('name','string',
        length=100,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Name is required")),
        label=T("Name"),
    ),
    Field('abbr', 'string',
        length=10,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
        label=T('Abbr'),
    ),
    Field('address','text',
        label=T("Address"),
    ),
    Field('availability', 'boolean',
        default=True,
        label=T("Available?"),
    ),
    Field('organic_unit','reference organic_unit',
        label=T("Organic unit"),
    ),
    format="%(name)s",
)
db.campus.organic_unit.requires = IS_IN_DB(db,'organic_unit.id',
    '%(name)s',zero=None
)

## buildings
db.define_table('building',
    Field('name','string',
        length=100,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Name is required")),
        label=T("Name"),
    ),
    Field('abbr', 'string',
        length=10,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
        label=T('Abbr'),
    ),
    Field('availability', 'boolean',
        default=True,
        label=T("Available?"),
    ),
    Field('campus', 'reference campus'),
    format="%(name)s",
)
db.building.campus.requires = IS_IN_DB(db, 'campus.id',
    '%(name)s', zero=None
)

## classroom
db.define_table('classroom',
    Field('name','string',
        length=100,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Name is required")),
        label=T("Name"),
    ),
    Field('c_size', 'integer',
        default=0,
        required=False,
        label=T("Size"),
    ),
    Field('availability', 'boolean',
        default=True,
        label=T("Available?"),
    ),
    Field('building', 'reference building'),
    format="%(name)s"
)
db.classroom.building.requires = IS_IN_DB(db, 'building.id',
    '%(name)s', zero=None
)


## payments
PAYMENT_PERIODICITY = {1 : "Unique"}
PAYMENT_TYPE = {
    1: "Bank account",
    2: "Credit card",
    3: "Cash"
}
db.define_table('payment_concept',
    Field('name','string',
        label=T('Name'),
        length=20,
    ),
    Field('periodicity', 'integer',
        label=T('Periodicity'),
        represent = lambda value,row: T(PAYMENT_PERIODICITY[value])
    ),
    Field('amount','double',
        label=T('Amount'),
        required=True,
    ),
    Field('status', 'boolean',
        default=True,
        required=True,
        label=T('Status'),
    ),
    format="%(name)s",
)
db.payment_concept.id.label=T("Code")
db.payment_concept.periodicity.requires = IS_IN_SET(PAYMENT_PERIODICITY,
    zero=None
)
db.payment_concept.amount.requires.append(IS_NOT_EMPTY())
db.payment_concept.name.requires = [IS_NOT_EMPTY(),
    IS_NOT_IN_DB(db, 'payment_concept.name')
]
db.define_table('payment',
    Field('person', 'reference person',
        label=T('Person'),
    ),
    Field('payment_concept', 'reference payment_concept',
        label=T('Concept'),
    ),
    Field('payment_date', 'datetime',
        label=T('Date & time'),
    ),
    Field('amount', 'double',
        label=T('Amount'),
    ),
    Field('receipt_number', 'integer',
        label=T('Receipt No.'),
        comment=T('Receipt Number')
    ),
)
db.define_table('payment_bank',
    Field('payment', 'reference payment',
        label=T('Payment'),
    ),
    Field('transaction_number', 'integer',
        label=T('Transaction number'),
    ),
)
db.define_table('payment_credit',
    Field('payment', 'reference payment'),
)
db.define_table('payment_cash',
    Field('payment', 'reference payment'),
)
db.payment.id.readable=False
db.payment.id.writable=False
db.payment.receipt_number.requires.append(IS_NOT_EMPTY())
db.payment.person.widget = SQLFORM.widgets.autocomplete(
    request, db.person.full_name,
    id_field=db.person.id,
    min_length=1,
)
db.payment_bank.transaction_number.requires.append(IS_NOT_EMPTY())
db.payment.amount.requires.append(IS_NOT_EMPTY())
db.payment.payment_date.requires = [IS_NOT_EMPTY(),
    IS_DATETIME()
]
db.payment.payment_concept.requires = IS_IN_DB(db, 'payment_concept.id',
    '%(name)s', zero=None
)
db.payment.person.requires = IS_IN_DB(db,'person.id',
    '%(full_name)s', zero=None
)

# acedemic level
db.define_table('academic_level',
    Field('name', 'string', label=T('Name'),
        required=True,
        notnull=True,
    ),
    format="%(name)s"
)
db.academic_level.id.label = T('ID')
db.academic_level.name.requires = [IS_NOT_EMPTY(),
    IS_NOT_IN_DB(db, 'academic_level.name'),
]

# courses (subjects/materias)
db.define_table('course',
    Field('name','string',
        length=100,
        required=True,
        requires=[IS_NOT_EMPTY(error_message=T("Name is required"))],
        label=T("Name"),
    ),
    Field('abbr', 'string',
        length=10,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Short name is required")),
        label=T('Abbr'),
    ),
    format='%(name)s',
)
db.course.name.requires.append(IS_NOT_IN_DB(db, 'course.name'))

# student group
db.define_table('student_group',
    Field('name','string',
        length=100,
        required=True,
        requires=[IS_NOT_EMPTY(error_message=T("Name is required"))],
        label=T("Name"),
    ),
    Field('academic_year', 'reference academic_year',
        label=T('Academic year'),
    ),
    Field('career_id', 'reference career',
        label=T('Career'),
    ),
    Field('academic_level', 'reference academic_level',
        label=T('Academic level'),
    ),
    Field('classroom', 'reference classroom',
        label=T('Classroom'),
    ),
    Field('availability', 'boolean',
        default=False,
        label=T("Available?"),
    ),
    format="%(name)s",
)
db.student_group.name.requires.append(IS_NOT_IN_DB(db, 'student_group.name'))
db.student_group.academic_year.requires = IS_IN_DB(db, 'academic_year.id',
    '%(a_year)s', zero=None
)
db.student_group.academic_level.requires = IS_IN_DB(db, 'academic_level.id',
    '%(name)s', zero=None
)
db.student_group.classroom.requires = IS_IN_DB(db, 'classroom.id',
    '%(name)s', zero=None
)

# granted student access spaces
db.define_table('gsa_spaces',
    Field('academic_year', 'reference academic_year',
        label=T('Academic year'),
    ),
    Field('career', 'reference career',
        label=T('Career'),
    ),
    Field('regime', 'reference ou_regime',
        label=T('Regime'),
    ),
    Field('amount', 'integer',
        label=T('Amount'),
        default=0,
    ),
)
#db.gsa_spaces.academic_year.requires = IS_IN_DB(db, 'academic_year.id')


def _academic_plan_format(r):
    return "AP{0}{1}{2}".format(r.career_id, r.academic_level_id, r.course_id)
db.define_table('academic_plan',
    Field('career_id', 'reference career',
        label=T('Career'),
    ),
    Field('academic_level_id', 'reference academic_level',
        label=T('Academic level'),
    ),
    Field('course_id', 'reference course',
        label=T('Course/Subject'),
    ),
    Field('status', 'boolean',
        default=False,
        label=T("Active ?"),
    ),
    format = _academic_plan_format
)

#department
db.define_table('department',
    Field('name','string',
        length=100,
        required=True,
        requires=IS_NOT_EMPTY(error_message=T("Name is required")),
        label=T("Name"),
    ),
    Field('organic_unit', 'reference organic_unit'),
    format="%(name)s",
)
db.department.organic_unit.requires = IS_IN_DB(db, 'organic_unit.id',
    '%(name)s', zero=None
)

# ou_event
db.define_table('ou_event',
    Field('name','string',
        length=100,
        required=True,
        unique=True,
        requires=IS_NOT_EMPTY(error_message=T("Name is required")),
        label=T("Name"),
    ),
    Field('ou_event_type', 'integer',
        required=True,
        label=T('Event type'),
    ),
    Field('start_date', 'date',
        required=True,
        notnull=True,
        label=T('Start date'),
    ),
    Field('end_date', 'date',
        required=True,
        notnull=True,
        label=T('End date'),
    ),
    Field('academic_year', 'reference academic_year'),
    Field('availability', 'boolean',
        default=True,
        label=T("Available?"),
    ),
    format="%(name)s"
)
db.ou_event.ou_event_type.requires = IS_IN_SET({
    1: T('Enrollment'),
    2: T('Registration'),
}, zero=None)
db.ou_event.academic_year.requires = IS_IN_DB(db, 'academic_year.id',
    '%(a_year)s', zero=None
)

######################################
# teachers
######################################
TEACHER_BIND_VALS = (
    ('0','Efectivo'),
    ('1','Colaborador'),
    ('2','Otros'),
)
TEACHER_CATEGORY_VALUES = (
    ('0', 'Instructor'),
    ('1', 'Asistente'),
    ('2', 'Auxiliar'),
    ('3', 'Asociado'),
    ('4', 'Titular'),
    ('5', 'Otros'),
)
TEACHER_DEGREE_VALUES = (
    ('0', 'Bacharelato'),
    ('1', 'Licenciatuara'),
    ('2', 'Mestrado'),
    ('3', 'Doutoramento'),
)
def _teacher_bind_represent(value, row):
    return T(TEACHER_BIND_VALS[int(value)][1]) + " ({0})".format(value)
def _teacher_category_represent(value, row):
    return T(TEACHER_CATEGORY_VALUES[int(value)][1]) + " ({0})".format(value)
def _teacher_degree_represent(value, row):
    return T(TEACHER_DEGREE_VALUES[int(value)][1]) + " ({0})".format(value)
def _teacher_format(row):
    person = db.person[row.person_id]
    return person.full_name
db.define_table('teacher',
    Field('person_id', 'reference person', label=T("Person")),
    Field('teacher_bind', 'string', length=1, label=T("Bind"),
        represent=_teacher_bind_represent,
    ),
    Field('teacher_category', 'string', length=1,label=T("Category"),
        represent=_teacher_category_represent,
    ),
    Field('teacher_degree', 'string', length=1, label=T("Degree"),
        represent=_teacher_degree_represent,
    ),
    # TODO: buscar palabra correcta en ingles
    Field('date_of_entry', 'date',label=T("Since")),
    Field('department_id', 'reference department',label=T("Department")),
    Field('status', 'boolean',
        default=True,
        label=T("Status"),
    ),
    format=_teacher_format,
)
db.teacher.department_id.requires = IS_IN_DB(db, 'department.id', "%(name)s",
    zero=None,
)
db.teacher.date_of_entry.requires.append(IS_NOT_EMPTY(
    error_message=T("Date of entry is required"),
))
db.teacher.teacher_bind.requires=IS_IN_SET(TEACHER_BIND_VALS,zero=None,)
db.teacher.teacher_category.requires=IS_IN_SET(
    TEACHER_CATEGORY_VALUES,zero=None,
)
db.teacher.teacher_degree.requires=IS_IN_SET(TEACHER_DEGREE_VALUES,zero=None,)
######################################

#####################################
# Teachers courses/subjects assignaments
#####################################

db.define_table('teacher_course',
    Field('teacher_id', 'reference teacher',
        label=T('Teacher')
    ),
    Field('academic_year_id', 'reference academic_year',
        label=T('Academic year')
    ),
    Field('ou_event_id', 'reference ou_event',
        label=T("Event"),
    ),
    Field('student_group_id', 'reference student_group',
        label=T("Group"),
    ),
    Field('status', 'boolean',
        default=True,
        label=T("Status"),
    ),
)

#####################################

## database initialization
row = db().select(db.auth_group.ALL).first()
if not row:
    # create default users groups
    gid = auth.add_group('users','All users')
    auth.settings.everybody_group_id = gid
    auth.add_group('administrators','Administrators of AGIS')
    # academic regions
    id=db.academic_region.insert(code='01',name='RA I')
    db.province.bulk_insert([
        {'code': '04','name': 'Luanda', 'ar_id': id},
        {'code': '18','name': 'Bengo', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='02',name='RA II')
    db.province.bulk_insert([
        {'code': '09','name': 'Benguela', 'ar_id': id},
        {'code': '06','name': 'Kwanza Sul', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='03',name='RA III')
    db.province.bulk_insert([
        {'code': '01','name': 'Cabinda','ar_id': id},
        {'code': '02','name': 'Zaire', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='04',name='RA IV')
    db.province.bulk_insert([
        {'code': '08','name': 'Lunda Norte', 'ar_id': id},
        {'code': '17','name': 'Lunda Sul', 'ar_id': id},
        {'code': '07','name': 'Malanje', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='05',name='RA V')
    db.province.bulk_insert([
        {'code': '10','name': 'Huambo', 'ar_id': id},
        {'code': '11','name': 'Bié', 'ar_id': id},
        {'code': '12','name': 'Moxico', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='06',name='RA VI')
    db.province.bulk_insert([
        {'code': '15','name': 'Huíla', 'ar_id': id},
        {'code': '14','name': 'Namibe', 'ar_id': id},
        {'code': '16','name': 'Cunene', 'ar_id': id},
        {'code': '13','name': 'Cuando Cubango', 'ar_id': id},
    ])
    id=db.academic_region.insert(code='07',name='RA VII')
    db.province.bulk_insert([
        {'code': '03','name': 'Uíge', 'ar_id': id},
        {'code': '05','name': 'Kwanza Norte', 'ar_id': id}
    ])
    ihe_id = db.IHE.insert(name='Example University',
        ar_id=id,
        classification='10',
        nature='1',
        registration_code='000'
    )
    tmp_prov = db(db.province.id > 0).select().first()
    db.organic_unit.insert(name='Example Organic Unit',
        province_id=tmp_prov.id,
        aggregation_level='1',
        classification='20',
        registration_code='000',
        IHE_asigg_code='00',
        IHE_id=ihe_id
    )
    db.identity_card_type.bulk_insert([
        {'name': 'Bilhete de Identidade'},
        {'name': 'Pasaporte'},
    ])
    # careers import
    db.career_des.import_from_csv_file(
        open(os.path.join(request.folder,'careers_des.csv'), 'r')
    )
    # regimes import
    db.regime.import_from_csv_file(
        open(os.path.join(request.folder,'db_regime.csv'), 'r')
    )
    # municipality import
    db.municipality.import_from_csv_file(
        open(os.path.join(request.folder,'db_municipality.csv'), 'r')
    )
    # commune import
    db.commune.import_from_csv_file(
        open(os.path.join(request.folder,'db_commune.csv'), 'r')
    )
    # special education needs import
    db.special_education.import_from_csv_file(
        open(os.path.join(request.folder,'db_special_education.csv'), 'r')
    )
    # Middle school types import
    db.middle_school_type.import_from_csv_file(
        open(os.path.join(request.folder,'db_middle_school_type.csv'), 'r')
    )
    # payment concepts
    db.payment_concept.insert(name="Inscripción",
        periodicity=1,
        amount=0.0
    )
else:
    auth.settings.everybody_group_id = row.id