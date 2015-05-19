# encoding: utf-8
from gluon import *
'''
Created on 18/5/2015

@author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
'''

class TablaRegionAcademica(object):
    '''
    Define esquema en la base de datos para las regiones academicas
    '''


    def __init__(self):
        super(TablaRegionAcademica, self).__init__()
        db = current.db
        T = current.T
        db.define_table('region_academica',
            Field('nombre', 'string',
                length=50,
                required=True,
                notnull=True,
                label=T('Nombre'),
            ),
            Field('codigo','string',
                length=2,
                required=True,
                notnull=True,
                unique=True,
                label=T('Código'),
                comment=T('Código de dos digitos'),
            ),
            format='%(nombre)s - %(codigo)s',
            singular=T('Region academica'),
            plural=T('Regiones academicas'),
        )