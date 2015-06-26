# -*- coding: utf-8 -*-
from applications.agis.modules import tools
from applications.agis.modules.db import campus
from applications.agis.modules.db import edificio
from applications.agis.modules.db import aula


sidenav.append(
    [T('Gestionar campus'), # Titulo del elemento
     URL('gestion_campus'), # url para el enlace
     ['gestion_campus'],] # en funciones estará activo este item
)

sidenav.append(
    [T('Gestionar edificios'), # Titulo del elemento
     URL('gestion_edificio'), # url para el enlace
     ['gestion_edificio'],] # en funciones estará activo este item
)

sidenav.append(
    [T('Gestionar aulas'), # Titulo del elemento
     URL('gestion_aula'), # url para el enlace
     ['gestion_aula'],] # en funciones estará activo este item
)

def index():
    redirect( URL( 'gestion_campus' ) )
    return dict(message="hello from infraestructura.py")

@auth.requires_membership('administrators')
def gestion_edificio():
    response.view = 'infraestructura/gestion_campus.html'
    manejo = edificio.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )

@auth.requires_membership('administrators')
def gestion_aula():
    response.view = 'infraestructura/gestion_campus.html'
    manejo = aula.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )

@auth.requires_membership('administrators')
def gestion_campus():
    manejo = campus.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )
