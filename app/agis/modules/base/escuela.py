# -*- coding: utf-8 -*-
import os
from gluon import *

class Escuela(object):
    '''
    Representa la escuela como un todo
    '''


    def __init__(self):
        super(Escuela, self).__init__()

    
    def inicializar(self):
        db = current.db
        if db(db.auth_user.id > 0).count() == 0:
            self._InicializarBaseDeDatos()

    
    def _InicializarBaseDeDatos(self):
        # crear el usuario administrador y al grupo de administradores
        db = current.db
        request = current.request
        auth = current.auth
        admin_rol = db.auth_group.insert(role='admin')
        todos = auth.add_group('users','All users')
        current.auth.settings.everybody_group_id = todos
        admin_user = db.auth_user.insert(
            email="admin@example.com",
            password=db.auth_user.password.validate('admin')[0],
        )
        db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
        # importar las regiones academicas desde el disco
        try:
            db.region_academica.import_from_csv_file(
                open(os.path.join(request.folder,'db_region_academica.csv'), 'r')
            )
        except Error:
            # Si no se pudieron importar los datos asumir que es necesario,
            # crear los primeros valores por defecto.
            db.region_academica.insert(
                nombre="Region Academica de ejemplo",
                code='01'
            )
        region = db.region_academica[1]
        # crear instancia de la escuela
        esc_id = db.escuela.insert(nombre="Ejemplo de nombre",
            ra_id=region, clasificacion="10", naturaleza="1",
            codigo_registro="000", codigo="101000"
        )
        # importar las provincias
        try:
            db.provincia.import_from_csv_file(
                open(os.path.join(request.folder,'db_provincia.csv'), 'r')
            )
        except Error:
            # Si no se pudieron importar los datos crear una provincia de 
            # ejemplo para poder crear la unidad organica de la escuela
            db.provincia.insert(
                nombre="Provincia de ejemplo",
                code='01'
            )


