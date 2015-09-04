# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage

def form_edit_user(user_id):
    """Genera un formulario para la edición de un usuario"""
    return CAT(T("formulario de edición - usuario"))

def form_create_user():
    """Genera formulario para crear usuario"""
    return CAT(T("formulario de creación - usuario"))
