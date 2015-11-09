# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules.db import region_academica as ra
from applications.agis.modules.db import descripcion_carrera as db_descripcion_carrera
from applications.agis.modules.db import regimen as tbl_regimen
from applications.agis.modules.db import tipos_ensennanza as tipo_escuela_media
from applications.agis.modules.db import escuela_media as tbl_escuela_media
from applications.agis.modules.db import municipio as tbl_municipio
from applications.agis.modules.db import provincia
from applications.agis.modules.db import comuna
from applications.agis.modules.db import tipo_documento_identidad as tbl_tipo_dni
from applications.agis.modules.db import discapacidad
from gui.pais import grid_pais
from applications.agis.modules.gui.mic import *

rol_admin = auth.has_membership(role=myconf.take('roles.admin'))

menu_lateral.append(
    Accion(T('Regiones Académicas'),
           URL('region_academica'),
           rol_admin),
    ['region_academica'])
menu_lateral.append(Accion(T('Países'), URL('paises'), rol_admin), ['paises'])
menu_lateral.append(
    Accion(T('Descripciones de carrera'),
           URL('descripcion_carrera'),
           rol_admin),
    ['descripcion_carrera'])
menu_lateral.append(
    Accion(T('Localidades'), URL('localidades'), rol_admin),
    ['localidades'])
menu_lateral.append(
    Accion(T('Regímenes'), URL('regimen'), rol_admin),
    ['regimen'])
menu_lateral.append(
    Accion(T('Tipos de Enseñanza Media'), URL('tipos_ensennaza'),
           rol_admin),
    ['tipos_ensennaza'])
menu_lateral.append(
    Accion(T('Escuelas de Enseñanza Media'),
           URL('escuela_media'),
           rol_admin),
    ['escuela_media'])
menu_lateral.append(
    Accion(T('Tipos de documento de identidad'),
           URL('tipo_documento_identidad'),
           rol_admin),
    ['tipo_documento_identidad'])
menu_lateral.append(
    Accion(T('Necesidades de educación especial'),
           URL('tipo_discapacidad'),
           rol_admin),
    ['tipo_discapacidad'])

menu_migas.append(Accion(T('Configuración'), '#', True))
menu_migas.append(
    Accion(T('General'), URL('general','index'), rol_admin))


def index():
    redirect(URL('region_academica'))
    return dict(message="hello from general.py",sidenav=sidenav)

@auth.requires(rol_admin)
def region_academica():
    menu_migas.append(T('Regiones Académicas'))
    response.title = T('Regiones Académicas')
    return dict(manejo=ra.obtener_manejo())

@auth.requires(rol_admin)
def paises():
    menu_migas.append(T('Países'))
    response.title = T('Países')
    return dict(manejo=grid_pais())

@auth.requires(rol_admin)
def descripcion_carrera():
    menu_migas.append(T('Descripciones de carrera'))
    response.title = T('Descripciones de carrera')
    return dict(manejo=db_descripcion_carrera.obtener_manejo())

@auth.requires(rol_admin)
def regimen():
    menu_migas.append(T('Regímenes'))
    response.title = T('Configuración - Regímenes')
    return dict(manejo=tbl_regimen.obtener_manejo())

@auth.requires(rol_admin)
def tipos_ensennaza():
    def protected_row(row):
        return row.uuid != tipo_escuela_media.ID_PROTEGIDO
    manejo = tools.manejo_simple(db.tipo_escuela_media,
        editable=protected_row, borrar=protected_row)
    menu_migas.append(T('Tipos de Enseñanza Media'))
    response.title = T('Configuración - Tipos de Enseñanza Media')
    return dict(manejo=manejo)

@auth.requires(rol_admin)
def escuela_media():
    menu_migas.append(T('Escuelas de Enseñanza Media'))
    response.title = T('Configuración - Escuelas de Enseñanza Media')
    return dict(manejo=tbl_escuela_media.obtener_manejo())

@auth.requires(rol_admin)
def tipo_documento_identidad():
    menu_migas.append(T('Tipos de documento de identidad'))
    response.title = T('Configuración - Tipos de documento de identidad')
    return dict(manejo=tbl_tipo_dni.obtener_manejo())

@auth.requires(rol_admin)
def tipo_discapacidad():
    menu_migas.append(T('Necesidades de educación especial'))
    response.title = T('Configuración - Necesidades de educación especial')
    return dict(manejo=discapacidad.obtener_manejo())

@auth.requires(rol_admin)
def localidades():
    def protected_row(row):
        return row.uuid not in [provincia.ID_PROTEGIDO,
                                tbl_municipio.ID_PROTEGIDO,
                                comuna.ID_PROTEGIDO]
    db.provincia.id.readable = False
    db.municipio.id.readable = False
    db.comuna.id.readable = False
    db.municipio.provincia_id.writable = False
    db.comuna.municipio_id.writable = False
    manejo = SQLFORM.smartgrid(db.provincia,
        linked_tables=['municipio','comuna'], showbuttontext=False,
        details=False, csv=False, #formstyle='bootstrap',
        maxtextlength=80,
        editable=protected_row,
        deletable=protected_row
    )
    menu_migas.append(T('Localidades'))
    response.title = T('Configuración - Localidades')
    return dict(manejo=manejo)

def obtener_municipios():
    """Cuando es llamado por AJAX retorna la lista de municipios según la provincia"""
    provincia_id = request.vars.provincia_id
    municipios = tbl_municipio.obtener_municipios(provincia_id)
    rs = ''
    for muni in municipios:
        op = OPTION(muni.nombre, _value=muni.id)
        rs += op.xml()
    return rs
