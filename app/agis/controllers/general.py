# -*- coding: utf-8 -*-
from gluon.tools import Crud
from applications.agis.modules.db import region_academica as ra
from applications.agis.modules.db import descripcion_carrera as db_descripcion_carrera
from applications.agis.modules.db import regimen as tbl_regimen
from applications.agis.modules.db import tipos_ensennanza as tipo_escuela_media
from applications.agis.modules.db import escuela_media as tbl_escuela_media
from applications.agis.modules.db import municipio as tbl_municipio
from applications.agis.modules.db import tipo_documento_identidad as tbl_tipo_dni
from applications.agis.modules.db import discapacidad

sidenav.append(
    [T('Regiones Académicas'), # Titulo del elemento
     URL('region_academica'), # url para el enlace
     ['region_academica'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Descripciones de carrera'), # Titulo del elemento
     URL('descripcion_carrera'), # url para el enlace
     ['descripcion_carrera'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Localidades'), # Titulo del elemento
     URL('localidades'), # url para el enlace
     ['localidades'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Regímenes'), # Titulo del elemento
     URL('regimen'), # url para el enlace
     ['regimen'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Tipos de Enseñanza Media'), # Titulo del elemento
     URL('tipos_ensennaza'), # url para el enlace
     ['tipos_ensennaza'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Escuelas de Enseñanza Media'), # Titulo del elemento
     URL('escuela_media'), # url para el enlace
     ['escuela_media'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Tipos de documento de identidad'), # Titulo del elemento
     URL('tipo_documento_identidad'), # url para el enlace
     ['tipo_documento_identidad'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Necesidades de educación especial'), # Titulo del elemento
     URL('tipo_discapacidad'), # url para el enlace
     ['tipo_discapacidad'],] # en funciones estará activo este item
)
crud = Crud(db)
#crud.settings.auth = auth
crud.settings.controller = 'general'

def index():
    redirect(URL('region_academica'))
    return dict(message="hello from general.py",sidenav=sidenav)

@auth.requires_membership('administrators')
def region_academica():
    return dict(sidenav=sidenav,manejo=ra.obtener_manejo())

@auth.requires_membership('administrators')
def descripcion_carrera():
    return dict(sidenav=sidenav,manejo=db_descripcion_carrera.obtener_manejo())

@auth.requires_membership('administrators')
def regimen():
    return dict(sidenav=sidenav,manejo=tbl_regimen.obtener_manejo())

@auth.requires_membership('administrators')
def tipos_ensennaza():
    def links(fila):
        out = CAT()
        a1,a2 = (None,None)
        if fila.id != tipo_escuela_media.ESPECIAL_ID:
            url1 = URL('tipos_ensennaza', args=[
                'delete',
                'tipo_escuela_media',
                fila.id
                ], user_signature=True)
            a1 = A(I("", _class="icon-trash"), _class="btn", _title=T("Borrar"),
                _href=url1)
            url2 = URL('tipos_ensennaza', args=[
                'edit',
                'tipo_escuela_media',
                fila.id
                ], user_signature=True)
            a2 = A(I("", _class="icon-edit"), _class="btn", _title=T("Edit"),
                   _href=url2)
        else:
            url1 = '#'
            a1 = A(I("", _class="icon-trash"), _class="btn disabled",
                   _title=T("Borrar"),
                   _href=url1)
            url2 = '#'
            a2 = A(I("", _class="icon-edit"), _class="btn disabled",
                   _title=T("Borrar"),
                   _href=url2)
        out.append(a1)
        out.append(' ')
        out.append(a2)
        return out
    response.view = "general/regimen.html"
    manejo = tipo_escuela_media.obtener_manejo(
            enlaces=[dict(header='',body=links)]
        )
    crud.settings.update_next = URL('tipos_ensennaza')
    crud.settings.delete_next = URL('tipos_ensennaza')
    if 'edit' in request.args:
        manejo = crud.update(db.tipo_escuela_media, request.args(2))
    elif 'delete' in request.args:
        manejo = crud.delete(db.tipo_escuela_media, request.args(2))
    return dict(sidenav=sidenav,manejo=manejo)

@auth.requires_membership('administrators')
def escuela_media():
    return dict(sidenav=sidenav,manejo=tbl_escuela_media.obtener_manejo())

@auth.requires_membership('administrators')
def tipo_documento_identidad():
    return dict(sidenav=sidenav, manejo=tbl_tipo_dni.obtener_manejo())

@auth.requires_membership('administrators')
def tipo_discapacidad():
    return dict(sidenav=sidenav, manejo=discapacidad.obtener_manejo())

@auth.requires_membership('administrators')
def localidades():
    db.provincia.id.readable = False
    db.municipio.id.readable = False
    db.comuna.id.readable = False
    db.municipio.provincia_id.writable = False
    db.comuna.municipio_id.writable = False
    manejo = SQLFORM.smartgrid(db.provincia,
        linked_tables=['municipio','comuna'],showbuttontext=False,details=False,csv=False,
        formstyle='bootstrap',maxtextlength=80,
    )
    return dict(sidenav=sidenav,manejo=manejo)

def obtener_municipios():
    """Cuando es llamado por AJAX retorna la lista de municipios según la provincia"""
    provincia_id = request.vars.provincia_id
    municipios = tbl_municipio.obtener_municipios(provincia_id)
    rs = ''
    for muni in municipios:
        op = OPTION(muni.nombre, _value=muni.id)
        rs += op.xml()
    return rs
