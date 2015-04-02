# -*- coding: utf-8 -*-

import os

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = None

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

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
    IS_MATCH('^\d{2,2}$', error_message=T('Invalid code')),
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
        comment=T("Two-digit province code"),
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
        length=9,compute=__comp_career_des_code,
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
db.define_table('career',
    Field('career_des_id', 'reference career_des',
        label=T('Career Description'),
    ),
    Field('organic_unit_id', 'reference organic_unit',
        label=T('Organic Unit'),
    ),
)
db.career.organic_unit_id.requires = IS_IN_DB(db,
    'organic_unit.id', '%(name)s', zero=None,
)
db.career.career_des_id.requires = IS_IN_DB(
    db,
    'career_des.id', '%(name)s', zero=None,
)


# regime
db.define_table('regime',
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
)
db.ou_regime.organic_unit_id.requires = IS_IN_DB(db,'organic_unit.id',
    '%(name)s',
    zero=T('Choose one'),
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
        length=6,
        required=True,
        unique=True,
        notnull=True,
        label=T('Code'),
        comment=T('Six digit code'),
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
    IS_MATCH('^\d{6,6}$', error_message=T('Code is not valid')),
    IS_NOT_IN_DB(db, 'municipality.code'),
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
    ),
    Field('name','string',
        length=200,
        required=True,
    ),
    format='%(name)s',
    plural=T('Special education needs'),
    singular=T('Special education need'),
)
db.special_education.code.requires = [
    IS_NOT_EMPTY(error_message=T('A code is required')),
    IS_NOT_IN_DB(db,'special_education.code',
        error_message=T('That special education need is alredy on database'),
    )
]
db.special_education.name.requires = [
    IS_NOT_EMPTY(error_message=T('A name is required')),
]

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
    # careers import
    db.career_des.import_from_csv_file(
        open(os.path.join(request.folder,'careers_des.csv'), 'r')
    )
    # Regimes
    db.regime.bulk_insert([
        {'name': 'Regular', 'abbr': 'R'},
        {'name': 'Pos-Laboral', 'abbr': 'P'}
    ])
else:
    auth.settings.everybody_group_id = row.id

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
