# -*- coding: utf-8 -*-

#  tblMunicipio.py
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



import tabla
import tblProvincia


from gluon import *


__all__ = ['TblMunicipio']


class TblMunicipio(tabla.Tabla):
    """Documentación"""

    def __init__(self):
        # importar e instanciar pre-requisitos antes de llamar a super
        self.provincia = tblProvincia.TblProvincia()
        super(TblMunicipio, self).__init__()


    def definirNombreDeTabla(self, nombre='municipio'):
        super(TblMunicipio, self).definirNombreDeTabla(nombre=nombre)


    def definirCampos(self):
        """Definir campos de la tabla"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('codigo','string',length=2,required=True,notnull=True,
                label=self.T('Codigo'),
                comment=self.T('Código de dos digitos'),
            ),
            Field('nombre','string',length=80,required=True,unique=True,
                notnull=True,label=self.T('Nombre'),
            ),
            Field('provincia_id', self.provincia.obtenerReferencia(),
                label=self.provincia.obtenerSingular(),
            ),
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = "%(nombre)s"
        self.tbl_plural = "Municipios"
        self.tbl_singular = "Municipio"
