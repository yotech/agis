# -*- coding: utf-8 -*-
from gluon import SQLFORM
from agiscore.gui.mic import grid_simple

def grid_carreras_ies(escuela, db, T):
    query  = (db.carrera_escuela.id > 0)
    db.carrera_escuela.id.readable = False
    orden = [db.carrera_escuela.descripcion_id]
    campos = [db.carrera_escuela.id,
              db.carrera_escuela.codigo,
              db.carrera_escuela.descripcion_id]
    text_length = {"carrera.escuela.descripcion_id": 100}
    return grid_simple(query,
                       fields=campos,
                       orderby=orden,
                       maxtextlength=text_length)