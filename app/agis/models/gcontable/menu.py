# -*- coding: utf-8 -*-
from agiscore.gui.mic import Accion

if not request.ajax and request.controller != 'appadmin':
    # import si se necesita
    from agiscore.gui.escuela import escuela_menu
    # contruir el menú en orden
    response.menu += escuela_menu()
    # response.menu += unidad_menu(int(request.args(0)))
