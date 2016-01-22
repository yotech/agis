# -*- coding: utf-8 -*-
from gluon import current
from gluon import Field
from gluon.validators import IS_NOT_EMPTY, IS_UPPER

from agiscore.db import unidad_organica

def definir_tabla(db=None, T=None):
    if db is None:
        db = current.db
    if T is None:
        T = current.T
    
    unidad_organica.definir_tabla()
    if not hasattr(db, 'turma'):
        tbl = db.define_table('turma',
            Field('nombre', 'string', length=50),
            Field('unidad_organica_id', 'reference unidad_organica')
            )
        
        tbl.nombre.label = T('Nombre')
        tbl.nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]