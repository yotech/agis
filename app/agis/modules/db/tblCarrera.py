# -*- coding: utf-8 -*-

#  tblCarrera.py
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
import tblUnidadOrganica
import tblDescripcionCarrera


from gluon import *


__all__ = ['TblCarrera']


class TblCarrera(tabla.Tabla):
    """Documentación"""

    def __init__(self):
        # importar e instanciar pre-requisitos antes de llamar a super
        self.tbl_uo = tblUnidadOrganica.TblUnidadOrganica()
        self.tbl_desp_carrera = tblDescripcionCarrera.TblDescripcionCarrera()
        super(TblCarrera, self).__init__()


    def definirNombreDeTabla(self, nombre='carrera'):
        super(TblCarrera, self).definirNombreDeTabla(nombre=nombre)


    @staticmethod
    def format(registro):
        uo = self.tbl_uo.obtener(id=registro['unidad_organica_id'])
        descripcion = self.tbl_desp_carrera.obtener(
            id=registro['descripcion_id']
        )
        return "{0} - {1}".format(descripcion.nombre,ou.nombre)
    

    def definirCampos(self):
        """Definir campos de la tabla"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('descripcion_id',
                self.tbl_desp_carrera.obtenerReferencia(),
                label=self.T('Descripción')
            ),
            Field('unidad_organica_id',
                self.tbl_uo.obtenerReferencia(),
                label=self.T('Unidad organica'),
            )
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = TblCarrera.format
        self.tbl_plural = "Carreras"
        self.tbl_singular = "Carrera"
