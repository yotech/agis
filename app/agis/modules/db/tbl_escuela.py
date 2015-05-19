# encoding: utf-8
from gluon import *
'''
Created on 18/5/2015

@author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
'''
import tbl_region_academica

def _comp_codigo_escuela(r):
    ar = db.region_academica[r['ra_id']]
    return ar.code + r['clasificacion'] + r['naturaleza'] + \
        r['codigo_registro']

class TablaEscuela(object):
    '''
    Define esquema para almacenar la información de la escuela
    '''


    def __init__(self):
        super(TablaEscuela, self).__init__()
        # la región academica es un pre-requisito de la escuela
        tbl_region_academica.TablaRegionAcademica()
        db = current.db
        T = current.T
        db.define_table('escuela',
            Field('nombre', 'string',
                length=100,
                required=True,
                label=T('nombre'),
            ),
            Field('ra_id', 'reference region_academica',
                ondelete='SET NULL',
                label=T('Región Academica'),
            ),
            Field('clasificacion','string',
                length=2,
                required=True,
                label=T('Clasificación'),
            ),
            Field('naturaleza','string',
                length=1,
                required=True,
                label=T('Naturaleza'),
            ),
            Field('codigo_registro','string',
                length=3,
                required=True,
                label=T('Código de Registro'),
                comment=T(
                    "Código de 3 digitos en el Ministerio"
                )
            ),
            Field('codigo',
                compute=_comp_codigo_escuela,
                notnull=True,
                label=T('Código'),
            ),
            Field('logo','upload',
                required=False,
                notnull=False,
                autodelete=True,
                uploadseparate=True,
                label=T('Logo'),
            ),
            format='%(nombre)s',
            singular=T('Instituto de educación superior'),
            plural=T('Institutos de educación superior'),
        )
    
    
    def obtener_registro(self):
        """Retorna el registro de la base de datos para la escuela"""
        db = current.db
        record = db(db.escuela.id>0).select().first()
        return record