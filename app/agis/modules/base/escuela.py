# -*- coding: utf-8 -*-
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
        admin_rol = db.auth_group.insert(role='admin')
        todos = auth.add_group('users','All users')
        current.auth.settings.everybody_group_id = gid
        admin_user = db.auth_user.insert(
            email="admin@example.com",
            password=db.auth_user.password.validate('admin')[0],
        )
        db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
        


