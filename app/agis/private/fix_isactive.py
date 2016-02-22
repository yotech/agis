#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arregla problema con el campo is_active, correrlo de la forma:

python web2py.py -S APP -M -R applications/APP/private/fix_isactive.py

cambiar APP por el nombre de aplicación que tenga agis.
"""

from gluon import *
from gluon.storage import Storage

for tbl in current.db:
    if hasattr(tbl, 'is_active') and ('archive' not in tbl._tablename):
        print "Procesando: {} ".format(tbl._tablename.upper()),
        for registro in current.db(tbl.id > 0,
                                   ignore_common_filters=True).select(tbl.ALL):
            if registro.is_active is None:
                registro.update_record(is_active=True)
        print "Done !"

current.db.commit()