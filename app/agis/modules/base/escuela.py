# -*- coding: utf-8 -*-
import os
from gluon import *
from applications.agis.modules.db import *


class Escuela(object):
    '''
    Representa la escuela como un todo
    '''


    def __init__(self):
        super(Escuela, self).__init__()
        self.db = current.db
        self.auth = current.auth
        self.T = current.T
        self.request = current.request
        self.inicializar()

    
    def inicializar(self):
        db = self.db
        if db(db.auth_user.id > 0).count() == 0:
            self._InicializarBaseDeDatos()
            # Después de incializar la BD logear al usuario admin para que
            # configure la escuela
            self.auth.login_bare('admin@example.com','admin')

    
    def _InicializarBaseDeDatos(self):
        # crear el usuario administrador y al grupo de administradores
        db = self.db
        request = self.request
        auth = self.auth
        admin_rol = db.auth_group.insert(role='admin')
        admin_user = db.auth_user.insert(
            email="admin@example.com",
            password=db.auth_user.password.validate('admin')[0],
        )
        db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
        db.commit()
        tbl_region = TblRegionAcademica()
        # importar las regiones academicas desde el disco
        try:
            tbl_region.importarDeArchivo(
                os.path.join(request.folder,'db_region_academica.csv')
            )
        except:
            tbl_region.insertar(
                nombre="Region Academica de ejemplo",
                codigo="01"
            )
        #try:
            #db.region_academica.import_from_csv_file(
                #open(os.path.join(request.folder,'db_region_academica.csv'), 'r')
            #)
        #except Error:
            ## Si no se pudieron importar los datos asumir que es necesario,
            ## crear los primeros valores por defecto.
            #db.region_academica.insert(
                #nombre="Region Academica de ejemplo",
                #code='01'
            #)
        #db.commit()
        #region = db.region_academica[1]
        ## crear instancia de la escuela
        #esc_id = db.escuela.insert(nombre="Ejemplo de nombre",
            #ra_id=region, clasificacion="10", naturaleza="1",
            #codigo_registro="000", codigo="101000"
        #)
        #db.commit()
        ## importar las provincias
        #try:
            #db.provincia.import_from_csv_file(
                #open(os.path.join(request.folder,'db_provincia.csv'), 'r')
            #)
        #except Error:
            ## Si no se pudieron importar los datos crear una provincia de 
            ## ejemplo para poder crear la unidad organica de la escuela
            #db.provincia.insert(
                #nombre="Provincia de ejemplo",
                #code='01'
            #)
        #db.commit()
        ## crear la unidad organica que represente la sede central de la escuela
        #provincia = db.provincia[1]
        #escuela = db.escuela[esc_id]
        #db.unidad_organica.insert(escuela_id=escuela.id,
            #provincia_id=provincia.id, nombre="Unidad Organica (por defecto)",
            #nivel_agregacion='1', # es la sede central
            #clasificacion='20', codigo_registro='000',
            #escuela_codigo='00', codigo=escuela.codigo+'120000'
        #)
        #db.commit()
        ## TODO: importar: carreras,municipios,comunas, ... etc
