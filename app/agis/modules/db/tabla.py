# -*- coding: utf-8 -*-
#
#  table.py
#  
#  Copyright 2015 Yoel Benítez Fonseca <ybenitezf@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from gluon import *


__all__ = ['Tabla']


class Tabla(object):
    """Clase base para las tablas de datos con DAL"""
    # nombre de la tabla en la base de datos
    tbl_nombre = ''
    # formato para referencias
    tbl_format = ''
    # texto para plural
    tbl_plural = ''
    # texto para valores únicos
    tbl_singular = ''
    # campos de la tabla
    tbl_campos = None
    # objeto en DAL para la tabla
    tbl = None


    def __init__(self):
        super(Tabla, self).__init__()
        self.db = current.db
        self.auth = current.auth
        self.T = current.T
        # hacer la definicion de la tabla
        self.definirTabla()


    def definirCampos(self):
        """Las derivaciones de esta clase deben encargarse de la definición de
        los campos para la tabla.

        por ejemplo:

            def definirCampos(self):
                self.tbl_campos = self.db.Table(self.db, 'mi_tabla',
                    Field('nombre', 'string')
                )

        Este método es llamado automáticamente por Tabla.__init__()
        """
        raise NotImplementedError()


    def definirNombreDeTabla(self, nombre=None):
        """define el nombre de la tabla con la cual se podrá referir a la misma
        mediante DAL

        Si no se establece un nombre se usara el nombre de la clase como nombre
        para la tabla
        """
        if not nombre:
            # si no se define un nombre tomar el nombre de la clase como nombre
            # para la tabla
            nombre = str(self.__class__)
            nombre = nombre.strip('><').rsplit(' ')[1].split('.')[-1].split("'")[0]
            self.tbl_nombre = nombre
        else:
            self.tbl_nombre = nombre


    def obtenerCampos(self):
        """Retorna el objeto que contiene las definiciones de los campos.

        ver 'dummy table' en la sección 6.29.1 del manual de web2py, el valor
        retornado puede usarse para contruir formularios.
        """
        return self.tbl_campos


    def definirTabla(self):
        """Ordena a DAL definir la tabla en la base de datos"""
        self.definirNombreDeTabla()
        self.definirCampos()
        self.tbl = self.db.define_table(self.tbl_nombre, self.tbl_campos,
            format=self.tbl_format, plural=self.T(self.tbl_plural),
            singular=self.T(self.tbl_singular)
        )
        # fijar la transacción y crear la tabla
        self.db.commit()

    def insertar(self, **campos):
        """ Subclases deben sobreescribir este método para validación de los
        valores de los campos.
        """
        id = self.tbl.insert(**campos)
        self.db.commit()
        return id

    def importarDeArchivo(self, nombre_archivo):
        """Importa los registros de la tabla del archivo 'nombre_archivo"""
        self.tbl.import_from_csv_file(open(nombre_archivo,'r'))
        self.db.commit()
