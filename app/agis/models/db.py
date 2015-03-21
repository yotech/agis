# -*- coding: utf-8 -*-

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
        notnull=True
    ),
    format='%(name)s - %(code)s',
    singular=T('Academic region'),
    plural=T('Academic regions'),
)
db.academic_region.name.requires = [
    IS_NOT_EMPTY(),
    IS_NOT_IN_DB(db,'academic_region.name'),
]

db.define_table('province',
    Field('name','string',
        length=2,
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
db.province.name.requires = [
    IS_NOT_EMPTY(),
    IS_NOT_IN_DB(db, 'province.name'),
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
        {'name': 'Luanda', 'ar_id': id},
        {'name': 'Bengo', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='02',name='RA II')
    db.province.bulk_insert([
        {'name': 'Benguela', 'ar_id': id},
        {'name': 'Kwanza Sul', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='03',name='RA III')
    db.province.bulk_insert([
        {'name': 'Cabinda', 'ar_id': id},
        {'name': 'Zaire', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='04',name='RA IV')
    db.province.bulk_insert([
        {'name': 'Lunda Norte', 'ar_id': id},
        {'name': 'Lunda Sul', 'ar_id': id},
        {'name': 'Malanje', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='05',name='RA V')
    db.province.bulk_insert([
        {'name': 'Huambo', 'ar_id': id},
        {'name': 'Bié', 'ar_id': id},
        {'name': 'Moxico', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='06',name='RA VI')
    db.province.bulk_insert([
        {'name': 'Huíla', 'ar_id': id},
        {'name': 'Namibe', 'ar_id': id},
        {'name': 'Cunene', 'ar_id': id},
        {'name': 'Cuando Cubango', 'ar_id': id},
    ])
    id=db.academic_region.insert(code='07',name='RA VII')
    db.province.bulk_insert([
        {'name': 'Uíge', 'ar_id': id},
        {'name': 'Kwanza Norte', 'ar_id': id}
    ])
else:
    auth.settings.everybody_group_id = row.id

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
