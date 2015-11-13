# -*- coding: utf-8 -*-
from gluon.storage import Storage
from agiscore import tools
from agiscore.db import campus
from agiscore.db import edificio
from agiscore.db import aula

rol_admin = auth.has_membership(myconf.take('roles.admin'))

menu_lateral.append(
    Accion(T('Gestionar campus'),
           URL('gestion_campus'), rol_admin),
    ['gestion_campus'])

menu_lateral.append(
    Accion(T('Gestionar edificios'),
           URL('gestion_edificio'), rol_admin),
    ['gestion_edificio'])

menu_lateral.append(
    Accion(T('Gestionar aulas'),
           URL('gestion_aula'), rol_admin),
    ['gestion_aula'])

menu_migas.append(Accion(T('Configuración'), '#', True))
menu_migas.append(
    Accion(T('Infraestructura'), URL('index'), rol_admin))

def index():
    redirect( URL( 'gestion_campus' ) )
    return dict(message="hello from infraestructura.py")

@auth.requires(rol_admin)
def gestion_edificio():
    menu_migas.append(T('Gestión de edificios'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = edificio.obtener_manejo()
    return dict(manejo=manejo )

@auth.requires(rol_admin)
def gestion_aula():
    menu_migas.append(T('Gestión de aulas'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = aula.obtener_manejo()
    return dict( manejo=manejo )

@auth.requires(rol_admin)
def gestion_campus():
    menu_migas.append(T('Gestión de campus'))
    manejo = campus.obtener_manejo()
    return dict( manejo=manejo )
