# -*- coding: utf-8 -*-
from applications.agis.modules.db import tipo_pago as tp

sidenav.append(
    [T('Tipos de Pagos'), # Titulo del elemento
     URL('tipo_pago'), # url para el enlace
     ['tipo_pago'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Registrar pago'), # Titulo del elemento
     URL('registrar_pago'), # url para el enlace
     ['registrar_pago'],] # en funciones estará activo este item
)

def index():
    return dict(message="hello from contabilidad.py")

@auth.requires_membership('administrators')
def registrar_pago():
    if not 'step' in request.vars:
        redirect( URL( 'registrar_pago',args=['1'] ) )
    step = request.vars.step
    manejo = tp.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo,step=step )

@auth.requires_membership('administrators')
def tipo_pago():
    manejo = tp.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )
