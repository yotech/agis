#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools
from db import pais as model

def grid_pais():
    db = current.db
    model.definir_tabla()
    db.pais.id.readable = False
    db.pais.id.writable = False
    return tools.manejo_simple(db.pais, [db.pais.codigo, db.pais.nombre])
