# -*- coding: utf-8 -*-
from applications.agis.modules.db import region_academica as ra
from applications.agis.modules.db import descripcion_carrera as db_descripcion_carrera


sidenav = []
sidenav.append(
    [T('Gestión de Regiones Académicas'), # Titulo del elemento
     URL('region_academica'), # url para el enlace
     ['region_academica'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Gestión carreras'), # Titulo del elemento
     URL('descripcion_carrera'), # url para el enlace
     ['descripcion_carrera'],] # en funciones estará activo este item
)


def index():
    redirect(URL('region_academica'))
    return dict(message="hello from general.py",sidenav=sidenav)

@auth.requires_membership('administrators')
def region_academica():
    return dict(sidenav=sidenav,manejo=ra.obtener_manejo())

@auth.requires_membership('administrators')
def descripcion_carrera():
    return dict(sidenav=sidenav,manejo=db_descripcion_carrera.obtener_manejo())
