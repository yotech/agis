# -*- coding: utf-8 -*-

from applications.agis.modules.db import escuela
from applications.agis.modules.db import unidad_organica

sidenav.append(
    [T('Escuela'), # Titulo del elemento
     URL('configurar_escuela'), # url para el enlace
     ['configurar_escuela'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Gestión de Unidades organicas'), # Titulo del elemento
     URL('gestion_uo'), # url para el enlace
     ['gestion_uo'],] # en funciones estará activo este item
)

def index():
    redirect(URL('default','index'))
    return dict(message="hello from instituto.py")

@auth.requires_membership('administrators')
def configurar_escuela():
    """Presenta formulario con los datos de la escuela y su sede cetral"""
    instituto = escuela.obtener_escuela()
    sede_central = escuela.obtener_sede_central(instituto)
    db.escuela.id.readable = False
    db.escuela.id.writable = False
    db.escuela.region_academica_id.comment = T(
        """
        Después de modificar este valor y guardar los cambios se debe corregir la provincia
        a la que pertenece la sede central de la escuela.
        """
    )
    db.unidad_organica.id.readable = False
    db.unidad_organica.id.writable = False
    db.unidad_organica.nivel_agregacion.writable = False
    db.unidad_organica.escuela_id.writable = False
    db.unidad_organica.escuela_id.comment = T('Representa la sede central de la escuela, no se puede modificar')

    # la unidad organica debe estar en una de las provincias de la región academica de la escuela.
    region = escuela.obtener_region(instituto)
    provincias = region_academica.obtener_provincias(region)
    valores = []
    for p in provincias:
        valores.append( (p.id, p.nombre) )
    db.unidad_organica.provincia_id.requires = IS_IN_SET(valores, zero=None)
    db.unidad_organica.provincia_id.comment=T(
        """
        Para actualizar este valor primero debe establecer la región academica de la
        escuela y luego fijar la provincia a la que pertenece su sede central
        """
    )
    #####

    form_escuela = SQLFORM( db.escuela,instituto,formstyle='bootstrap' )
    form_uo = SQLFORM( db.unidad_organica,sede_central,formstyle='bootstrap' )
    response.title = T("Configurar escuela")
    if form_escuela.process().accepted:
        session.flash = T("Cambios guardados")
        redirect('configurar_escuela')
    if form_uo.process().accepted:
        session.flash = T("Cambios guardados")
        redirect('configurar_escuela')
    return dict(form_escuela=form_escuela,form_uo=form_uo, sidenav=sidenav)

@auth.requires_membership('administrators')
def gestion_uo():
    """Vista para la gestión de las unidades organicas"""
    instituto = escuela.obtener_escuela()
    manejo = unidad_organica.obtener_manejo(instituto.id)
    return dict(manejo=manejo,sidenav=sidenav)
