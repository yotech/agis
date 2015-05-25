#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tblRegionAcademica.py
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


from gluon import *


__all__ = ['TblRegionAcademica']


class TblRegionAcademica(tabla.Tabla):
    """ Representa una Región Academica """


    def __init__(self):
        super(TblRegionAcademica, self).__init__()


    def definirNombreDeTabla(self, nombre='region_academica'):
        # como convención usar el mismo nombre de la clase en notación de
        # guion bajo.
        super(TblRegionAcademica, self).definirNombreDeTabla(nombre=nombre)


    def definirCampos(self):
        """Define los campos de region_academica"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('nombre', 'string',
                length=50,
                required=True,
                notnull=True,
                label=self.T('Nombre'),
            ),
            Field('codigo', 'string',
                length=2,
                required=True,
                notnull=True,
                unique=True,
                label=self.T('Código'),
                comment=self.T('Código de dos digitos'),
            ),
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = "%(codigo)s - %(nombre)s"
        self.tbl_plural = "Regiones academicas"
        self.tbl_singular = "Región academica"


    def insertar(self, **valores):
        nombre = valores['nombre']
        codigo = valores['codigo']
        return super(TblRegionAcademica, self).insertar(
            nombre=nombre,
            codigo=codigo
        )
