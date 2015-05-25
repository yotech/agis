# -*- coding: utf-8 -*-

#  tblUnidadOrganica.py
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
import tblEscuela


from gluon import *


__all__ = ['TblUnidadOrganica']


class TblUnidadOrganica(tabla.Tabla):
    """Tabla en la base de datos para unidad organica"""

    def __init__(self):
        # importar e instanciar pre-requisitos antes de llamar a super
        self.tbl_escuela = tblEscuela.TblEscuela()
        self.tbl_provincia = tblProvincia.TblProvincia()
        super(TblUnidadOrganica, self).__init__()


    def definirNombreDeTabla(self, nombre='unidad_organica'):
        super(TblUnidadOrganica, self).definirNombreDeTabla(nombre=nombre)


    @staticmethod
    def _calcularCodigo(valores):
        esc = (tblEscuela.TblEscuela()).obtener(id=valores['escuela_id'])
        return (esc.codigo + valores['nivel_agregacion'] +
            valores['clasificacion'] + valores['codigo_registro']
        )


    def insertar(self, **valores):
        if 'codigo' not in valores.keys():
            valores['codigo'] = TblUnidadOrganica._calcularCodigo(valores)
        super(TblUnidadOrganica, self).insertar(**valores)


    def definirCampos(self):
        """Definir campos de la tabla unidad_organica"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('codigo',compute=TblUnidadOrganica._calcularCodigo,
                notnull=True,label=self.T('Código'),
            ),
            Field('nombre','string',required=True,notnull=True,length=100,
                label=self.T('Nombre'),
            ),
            Field('direccion','text',required=False,notnull=False,
                label=self.T('Dirección'),
            ),
            Field('provincia_id', self.tbl_provincia.obtenerReferencia(),
                label=self.T('Provincia')
            ),
            Field('nivel_agregacion','string',required=True,
                label=self.T('Nivel de agregación'),length=1,
            ),
            Field('clasificacion','string',length=2,required=True,
                label=self.T('Clasificación'),
            ),
            Field('codigo_registro','string',length=3,required=True,
                label=self.T('Código de registro'),
                comment=self.T(
                    "Código de registro en el ministerio"
                )
            ),
            Field('escuela_codigo','string',length=2,
                label=self.T('Código de Escuela'),
                required=True,notnull=True,
                comment=self.T(
                    "Código asignado por la escuela a la unidad organica"
                )
            ),
            Field('escuela_id', self.tbl_escuela.obtenerReferencia(),
                label=self.T('Escuela'),
                required=True,
            ),
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = "%(nombre)s"
        self.tbl_plural = "Unidades organicas"
        self.tbl_singular = "Unidad organica"
