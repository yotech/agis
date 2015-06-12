# -*- coding: utf-8 -*-

from applications.agis.modules import tools
from applications.agis.modules.db import escuela
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import regimen_uo

sidenav.append(
    [T('Escuela'), # Titulo del elemento
     URL('configurar_escuela'), # url para el enlace
     ['configurar_escuela'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Unidades organicas'), # Titulo del elemento
     URL('gestion_uo'), # url para el enlace
     ['gestion_uo'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Régimen a realizar en la UO'), # Titulo del elemento
     URL('asignar_regimen'), # url para el enlace
     ['asignar_regimen'],] # en funciones estará activo este item
)

def index():
    redirect(URL('configurar_escuela'))
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
def asignar_regimen():
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    db.regimen_unidad_organica.unidad_organica_id.default = unidad_organica_id
    db.regimen_unidad_organica.unidad_organica_id.writable = False
    db.regimen_unidad_organica.id.readable = False
    query = (db.regimen_unidad_organica.unidad_organica_id ==  unidad_organica_id)
    if 'new' in request.args:
        # preparar para agregar un nuevo elemento
        posibles_regimenes = regimen_uo.obtener_posibles(unidad_organica_id)
        if posibles_regimenes:
            db.regimen_unidad_organica.regimen_id.requires = IS_IN_SET( posibles_regimenes, zero=None )
        else:
            session.flash = T("Ya se han asociados todos los posibles regímenes a la UO")
            redirect(URL('asignar_regimen',vars={'unidad_organica_id': unidad_organica_id}))
    manejo = tools.manejo_simple(query,editable=False)
    return dict(sidenav=sidenav,manejo=manejo,select_uo=select_uo)

@auth.requires_membership('administrators')
def gestion_uo():
    """Vista para la gestión de las unidades organicas"""
    instituto = escuela.obtener_escuela()
    manejo = unidad_organica.obtener_manejo(instituto.id)
    return dict(manejo=manejo,sidenav=sidenav)
