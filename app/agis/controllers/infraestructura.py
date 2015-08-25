# -*- coding: utf-8 -*-
from gluon.storage import Storage
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
migas.append(
    tools.split_drop_down(
        Storage(dict(url='#', texto=T('Configuración'))),
        [Storage(dict(url=URL('general','index'),
                      texto=T('General'))),
         Storage(dict(url=URL('instituto','index'),
                      texto=T('Instituto'))),
         Storage(dict(url=URL('infraestructura','index'),
                      texto=T('Infraestructura'))),
         ]
        )
    )
migas.append(A(T('Infraestructura'), _href=URL('index')))

def index():
    redirect( URL( 'gestion_campus' ) )
    return dict(message="hello from infraestructura.py")

@auth.requires_membership('administrators')
def gestion_edificio():
    migas.append(T('Gestión de edificios'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = edificio.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )

@auth.requires_membership('administrators')
def gestion_aula():
    migas.append(T('Gestión de aulas'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = aula.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )

@auth.requires_membership('administrators')
def gestion_campus():
    migas.append(T('Gestión de campus'))
    manejo = campus.obtener_manejo()
    return dict( sidenav=sidenav, manejo=manejo )
