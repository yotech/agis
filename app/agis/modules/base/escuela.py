# -*- coding: utf-8 -*-
import os
from gluon import *
# cargar las definiciones de tablas
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
        # define la tabla para las regiones academicas
        tbl_region = TblRegionAcademica()
        # importar las regiones academicas desde el disco
        try:
            tbl_region.importarDeArchivo(
                os.path.join(request.folder,'db_region_academica.csv')
            )
        except:
            # si no se pudo importar ninguna se crea una por defecto
            tbl_region.insertar(
                nombre="Region Academica de ejemplo",
                codigo="01"
            )
        # representasión de la escuela en la BD
        tbl_escuela = TblEscuela()
        region = tbl_region.obtener(id=1)
        tbl_escuela.insertar(nombre="Ejemplo de nombre",
            ra_id=region.id, clasificacion="10", naturaleza="1",
            codigo_registro="000"
        )
        ## importar las provincias
        tbl_provincias = TblProvincia()
        try:
            tbl_provincias.importarDeArchivo(
                os.path.join(request.folder,'db_provincia.csv')
            )
        except:
            # Si no se pudieron importar los datos crear una provincia de 
            # ejemplo para poder crear la unidad organica de la escuela
            tbl_provincias.insertar(
                nombre="Provincia de ejemplo",
                codigo='01',
                ra_id=region.id,
            )
        # para crear la unidad organica de ejemplo
        provincia = tbl_provincias.obtener(id=1)
        escuela = tbl_escuela.obtener(id=1)
        tbl_uo = TblUnidadOrganica()
        tbl_uo.insertar(escuela_id=escuela.id,
            provincia_id=provincia.id, nombre="Unidad Organica (por defecto)",
            nivel_agregacion='1', # es la sede central
            clasificacion='20', codigo_registro='000',
            escuela_codigo='00'
        )
        ## TODO: importar: carreras,municipios,comunas, ... etc
        tbl_municipio = TblMunicipio()
        municipio_csv = os.path.join(request.folder,'db_municipality.csv')
        tbl_comuna = TblComuna()
        comunas_csv = os.path.join(request.folder,'db_commune.csv')
        try:
            tbl_municipio.importarDeArchivo(municipio_csv)
            tbl_comuna.importarDeArchivo(comunas_csv)
        except:
            # TODO: pasar salida al log de web2py
            print "Error importando datos"
