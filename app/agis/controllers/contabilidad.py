# -*- coding: utf-8 -*-
from applications.agis.modules.db import tipo_pago as tp

sidenav.append(
    [T('Tipos de Pagos'), # Titulo del elemento
     URL('tipo_pago'), # url para el enlace
     ['tipo_pago'],] # en funciones estará activo este item
)

def index():
    return dict(message="hello from contabilidad.py")

@auth.requires_membership('administrators')
def tipo_pago():
    manejo = tp.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )
