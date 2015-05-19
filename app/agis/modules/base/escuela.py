# -*- coding: utf-8 -*-
from gluon import *
# importar definiciones de tablas
from applications.agis.modules.db.tbl_escuela import TablaEscuela

class Escuela(object):
    '''
    Representa la escuela como un todo
    '''
    record = None

    def __init__(self):
        super(Escuela, self).__init__()
        # carga esquema de la base de datos
        esc = TablaEscuela()
        self.record = esc.obtener_registro()
        if not self.record:
            # inicializar la base de datos, crear los registros iniciales.
            self._InicializarBaseDeDatos()

    def __str__(self):
        return record.nombre
    
    
    def _InicializarBaseDeDatos(self):
        # crear el usuario administrador
        db = current.db
        admin_rol = db.auth_group.insert(role='admin')
        admin_user = db.auth_user.insert(
            email="admin@example.com",
            password=db.auth_user.password.validate('admin')[0],
        )
        db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
