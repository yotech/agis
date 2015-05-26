# -*- coding: utf-8 -*-

#  tblDescripcionCarrera.py
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


__all__ = ['TblDescripcionCarrera']


class TblDescripcionCarrera(tabla.Tabla):
    """Descriociones de las carreras según el ministerio de educación"""

    def __init__(self):
        # importar e instanciar pre-requisitos antes de llamar a super
        super(TblDescripcionCarrera, self).__init__()


    def definirNombreDeTabla(self, nombre='descripcion_carrera'):
        super(TblDescripcionCarrera, self).definirNombreDeTabla(nombre=nombre)


    @staticmethod
    def calcularCodigo(registro):
        return "{0}{1}{2}{3}".format(registro['cod_mes'],registro["cod_pnfq"],
            registro["cod_unesco"],registro["cod_career"]
        )


    def insertar(self, **valores):
        if 'codigo' not in valores.keys():
            valores['codigo'] = TblDescripcionCarrera.calcularCodigo(valores)
        super(TblDescripcionCarrera, self).insertar(**valores)
        

    def definirCampos(self):
        """Definir campos de la tabla"""
        self.tbl_campos = self.db.Table(self.db, self.obtenerAtributoCampos(),
            Field('nombre','string',length=100,label=self.T('Nombre'),
                notnull=True,required=True
            ),
            Field('cod_mes','string',length=1,label='MES',
                notnull=True,required=True,
            ),
            Field('cod_pnfq','string',length=2,label='PNFQ',
                notnull=True,required=True,
            ),
            Field('cod_unesco','string',length=3,label='UNESCO',
                notnull=True,required=True,
            ),
            Field('cod_career','string',length=3,
                label=self.T('Career code'),
                notnull=True,required=True,
            ),
            Field('codigo', 'string',
                length=9,label=self.T('Código'),
                compute=TblDescripcionCarrera.calcularCodigo,
                notnull=True,required=False,unique=True
            ),
        )
        # se puden usar definirCampos y definirNombre para asignar los valores
        # a estos atributos antes de que se defina la tabla en DAL
        self.tbl_format = "%(nombre)s"
        self.tbl_plural = "Descripciones de carreras"
        self.tbl_singular = "Descripcion de carrera"
