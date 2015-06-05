#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def tiene_rol(roles):
    """
    Retorna True si el usuario actual tiene alguno de los roles
    """
    auth = current.auth
    if auth.user:
        for rol in roles:
            if auth.has_membership(None, auth.user.id, rol):
                return True
    return False

def buscar_hijos(menu, elemento):
    """
    Busca dentro de menu algún elemento que coincida con elemento y retorna la lista de
    subitems de ese elemento
    """
    for item in menu:
        if item[0] == elemento:
            return item[3]
        else:
            if len(item[3]):
                return buscar_hijos(item[3], elemento)

def agregar_elemento(menu, opcion, roles, padre=None):
    """
    Agrega un item al menu si el usuario actual tiene alguno de los roles

    menu: menu al que se agrega la opcion
    opcion: item a agregar
    roles: lista de roles a comprobar
    padre: si opcion va a ser parte del submenu de padre
    """
    if tiene_rol( roles ):
        if not padre:
            agregar_en = menu
        else:
            agregar_en = buscar_hijos( menu, padre )

        if isinstance(opcion, tuple):
            agregar_en.append( opcion )
        else:
            # se asume que nos pasaron solamante el nombre de la opción
            # de la forma T('nombre')
            agregar_en.append( (opcion, False, '#', []) )
