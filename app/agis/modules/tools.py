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


def inicializar_base_datos():
    db = current.db
    request = current.request
     # academic regions
    id=db.academic_region.insert(code='01',name='RA I')
    db.province.bulk_insert([
        {'code': '04','name': 'Luanda', 'ar_id': id},
        {'code': '18','name': 'Bengo', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='02',name='RA II')
    db.province.bulk_insert([
        {'code': '09','name': 'Benguela', 'ar_id': id},
        {'code': '06','name': 'Kwanza Sul', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='03',name='RA III')
    db.province.bulk_insert([
        {'code': '01','name': 'Cabinda','ar_id': id},
        {'code': '02','name': 'Zaire', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='04',name='RA IV')
    db.province.bulk_insert([
        {'code': '08','name': 'Lunda Norte', 'ar_id': id},
        {'code': '17','name': 'Lunda Sul', 'ar_id': id},
        {'code': '07','name': 'Malanje', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='05',name='RA V')
    db.province.bulk_insert([
        {'code': '10','name': 'Huambo', 'ar_id': id},
        {'code': '11','name': 'Bié', 'ar_id': id},
        {'code': '12','name': 'Moxico', 'ar_id': id}
    ])
    id=db.academic_region.insert(code='06',name='RA VI')
    db.province.bulk_insert([
        {'code': '15','name': 'Huíla', 'ar_id': id},
        {'code': '14','name': 'Namibe', 'ar_id': id},
        {'code': '16','name': 'Cunene', 'ar_id': id},
        {'code': '13','name': 'Cuando Cubango', 'ar_id': id},
    ])
    id=db.academic_region.insert(code='07',name='RA VII')
    db.province.bulk_insert([
        {'code': '03','name': 'Uíge', 'ar_id': id},
        {'code': '05','name': 'Kwanza Norte', 'ar_id': id}
    ])
    ihe_id = db.IHE.insert(name='Example University',
        ar_id=id,
        classification='10',
        nature='1',
        registration_code='000'
    )
    tmp_prov = db(db.province.id > 0).select().first()
    db.organic_unit.insert(name='Example Organic Unit',
        province_id=tmp_prov.id,
        aggregation_level='1',
        classification='20',
        registration_code='000',
        IHE_asigg_code='00',
        IHE_id=ihe_id
    )
    db.identity_card_type.bulk_insert([
        {'name': 'Bilhete de Identidade'},
        {'name': 'Pasaporte'},
    ])
    # careers import
    db.career_des.import_from_csv_file(
        open(os.path.join(request.folder,'careers_des.csv'), 'r')
    )
    # regimes import
    db.regime.import_from_csv_file(
        open(os.path.join(request.folder,'db_regime.csv'), 'r')
    )
    # municipality import
    db.municipality.import_from_csv_file(
        open(os.path.join(request.folder,'db_municipality.csv'), 'r')
    )
    # commune import
    db.commune.import_from_csv_file(
        open(os.path.join(request.folder,'db_commune.csv'), 'r')
    )
    # special education needs import
    db.special_education.import_from_csv_file(
        open(os.path.join(request.folder,'db_special_education.csv'), 'r')
    )
    # Middle school types import
    db.middle_school_type.import_from_csv_file(
        open(os.path.join(request.folder,'db_middle_school_type.csv'), 'r')
    )
    # payment concepts
    db.payment_concept.insert(name="Inscripción",
        periodicity=1,
        amount=0.0
    )
