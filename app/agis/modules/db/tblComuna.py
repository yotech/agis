# -*- coding: utf-8 -*-

#  tblComuna.py
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
import tblMunicipio


from gluon import *


__all__ = ['TblComuna']


class TblComuna(tabla.Tabla):
    """Documentación"""

    def __init__(self):
        # importar e instanciar pre-requisitos antes de llamar a super
        self.municipio = tblMunicipio.TblMunicipio()
        super(TblComuna, self).__init__()


    def definirNombreDeTabla(self, nombre='comuna'):
        super(TblComuna, self).definirNombreDeTabla(nombre=nombre)


    def definirCampos(self):
        """Definir campos de la tabla"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('codigo','string',length=2,label=self.T('Código'),
                required=True,notnull=True,
            ),
            Field('nombre','string',length=100,label=self.T('Nombre'),
                required=True,notnull=True,
            ),
            Field('municipio_id', self.municipio.obtenerReferencia(),
                required=True,label=self.municipio.obtenerSingular(),
            ),
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = "%(nombre)s"
        self.tbl_plural = "Comunas"
        self.tbl_singular = "Comuna"
