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

def buscar_lista_hijos(menu, elemento):
    """
    Busca dentro de menu algún elemento que coincida con elemento y retorna la lista de
    subitems de ese elemento
    """
    hijos = None
    for item in menu:
        if (item[0]).xml() == elemento.xml():
            hijos = item[3] # encontre el padre, retorno la lista de hijos
            return hijos
        else:
            hijos = buscar_lista_hijos(item[3], elemento)
            if hijos != None:
                # si no es un hijo de item[0]
                # entonces probar con el proximo item
                return hijos
    return hijos

def agregar_elemento(menu, opcion, roles, padre=None):
    """
    Agrega un item al menu si el usuario actual tiene alguno de los roles

    menu: menu al que se agrega la opcion
    opcion: item a agregar debe ser una tuplade 4 elementos (texto, False, url, [])
    roles: lista de roles a comprobar
    padre: si opcion va a ser parte del submenu de padre
    """
    if tiene_rol( roles ):
        if not padre:
            agregar_en = menu
        else:
            agregar_en = buscar_lista_hijos( menu, padre )
            if agregar_en == None:
                return

        agregar_en.append( opcion )
