#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tblProvincia.py
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
import tblRegionAcademica

from gluon import *

__all__ = ['TblProvincia']

class TblProvincia(tabla.Tabla):
    """ Representa una Provincia """


    def __init__(self):
        # cargar pre-requisitos
        self.ra = tblRegionAcademica.TblRegionAcademica()
        super(TblProvincia, self).__init__()


    def definirNombreDeTabla(self, nombre='provincia'):
        super(TblProvincia, self).definirNombreDeTabla(nombre)


    def definirCampos(self):
        """Define los campos asociados a provincia"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('codigo','string',
                length=2,
                unique=True,
                required=True,
                label=self.T('Codigo'),
                comment=self.T("Codigo de 2 digitos"),
            ),
            Field('nombre','string',
                length=50,
                required=True,
                notnull=True,
                label=self.T('Nombre'),
            ),
            Field('ra_id', self.ra.obtenerReferencia(),
                ondelete='SET NULL',
                label=self.ra.obtenerSingular(),
            ),
        )
        self.tbl_format = "%(nombre)s"
        self.tbl_singular = "Provincia" # la traducción se realiza luego
        self.tbl_plural = "Provincias"
    
