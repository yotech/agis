#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from gluon import *


def inicializar_administrador():
    db = current.db
    auth = current.auth
    admin_rol = db.auth_group.insert(role='administrators')
    admin_user = db.auth_user.insert(
        email="admin@example.com",
        password=db.auth_user.password.validate('admin')[0],
    )
    db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
    db.commit()
    auth.login_bare('admin@example.com','admin')

def probar_base_de_datos():
    """Retorna True si la base de datos ya esta inicializada"""
    db = current.db
    if db(db.auth_user.id > 0).count() > 0:
        return True
    # en cc retornar Falso
    return False

def manejo_simple(conjunto,orden=[],longitud_texto=100):
    manejo = SQLFORM.grid(conjunto,
        details=False,
        csv=False,
        searchable=False,
        showbuttontext=False,
        maxtextlength=longitud_texto,
        orderby=orden,
        formstyle='bootstrap',
    )
    return manejo

def inicializar_base_datos():
    db = current.db
    request = current.request
    # academic regions
    db.region_academica.import_from_csv_file(
        open(os.path.join(request.folder,'db_region_academica.csv'), 'r')
    )
    db.provincia.import_from_csv_file(
        open(os.path.join(request.folder,'db_provincia.csv'), 'r')
    )
    region = db.region_academica[1]
    escuela = db.escuela.insert(nombre='Escuela (defecto)',
        region_academica_id=region.id,
        clasificacion='10',
        naturaleza='1',
        codigo_registro='000',
        codigo='07101000'
    )
    tmp_prov = db.provincia[1]
    db.unidad_organica.insert(nombre='Sede central (defecto)',
        provincia_id=tmp_prov.id,
        nivel_agregacion='1',
        clasificacion='20',
        codigo_registro='000',
        codigo_escuela='00',
        escuela_id=escuela
    )
    db.descripcion_carrera.import_from_csv_file(
        open(os.path.join(request.folder,'careers_des.csv'), 'r')
    )
    # municipios
    db.municipio.import_from_csv_file(
        open(os.path.join(request.folder,'db_municipality.csv'), 'r')
    )
    # comunas
    db.comuna.import_from_csv_file(
        open(os.path.join(request.folder,'db_commune.csv'), 'r')
    )
    # regímenes
    db.regimen.import_from_csv_file(
        open(os.path.join(request.folder,'db_regime.csv'), 'r')
    )
    # tipos de enseñanza media
    db.tipo_escuela_media.import_from_csv_file(
        open(os.path.join(request.folder,'db_middle_school_type.csv'), 'r')
    )
    db.tipo_documento_identidad.bulk_insert([
        {'nombre': 'Bilhete de Identidade'},
        {'nombre': 'Pasaporte'},
    ])
    # tipos de discapacidad
    db.discapacidad.import_from_csv_file(
        open(os.path.join(request.folder,'db_special_education.csv'), 'r')
    )
#     # special education needs import
#     db.special_education.import_from_csv_file(
#         open(os.path.join(request.folder,'db_special_education.csv'), 'r')
#     )

#     # payment concepts
#     db.payment_concept.insert(name="Inscripción",
#         periodicity=1,
#         amount=0.0
#     )
    db.commit()
