#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tblEscuela.py
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


__all__ = ['TblEscuela']


class TblEscuela(tabla.Tabla):
    """Almacena los datos de las escuelas"""

    def __init__(self):
        # cargar pre-requisitos antes de llamar a super
        self.ra = tblRegionAcademica.TblRegionAcademica()
        super(TblEscuela, self).__init__();


    def definirNombreDeTabla(self, nombre='escuela'):
        super(TblEscuela, self).definirNombreDeTabla(nombre=nombre)


    @staticmethod
    def _codigoEscuela(registro):
        """calcula el codigo para la escuela"""

        # necesario pq el método es estatico
        ra = tblRegionAcademica.TblRegionAcademica()
        # código de la región académica
        ra_codigo = (ra.obtener(id=registro['ra_id'])).codigo
        return ra_codigo + registro['clasificacion'] + \
            registro['naturaleza'] + \
            registro['codigo_registro']


    def insertar(self, **valores):
        if 'codigo' not in valores.keys():
            valores['codigo'] = TblEscuela._codigoEscuela(valores)
        super(TblEscuela, self).insertar(**valores)


    def definirCampos(self):
        """define los campos de la tabla escuela"""
        
        # nombre del conjunto temporal de campos
        n_tmp = '{0}_campos'.format(self.obtenerNombreDeTabla())
        self.tbl_campos = self.db.Table(self.db, n_tmp,
            Field('nombre','string',length=100,required=True,
                label=self.T('Nombre'),
            ),
            Field('ra_id', self.ra.obtenerReferencia(), ondelete='SET NULL',
                label=self.ra.obtenerSingular(),
            ),
            Field('clasificacion', 'string',
                length=2,
                required=True,
                label=self.T('Clasificación'),
            ),
            Field('naturaleza', 'string',
                length=1,
                required=True,
                label=self.T('Naturaleza'),
            ),
            Field('codigo_registro', 'string',
                length=3,
                required=True,
                label=self.T('Código de Registro'),
                comment=self.T(
                    "Código de 3 digitos en el Ministerio"
                )
            ),
            Field('codigo',
                compute=TblEscuela._codigoEscuela,
                notnull=True,
                label=self.T('Código'),
            ),
            Field('logo', 'upload',
                required=False,
                notnull=False,
                autodelete=True,
                uploadseparate=True,
                label=self.T('Logo'),
            ),
        )
        self.tbl_format="%(nombre)s"
        self.tbl_plural="Escuelas"
        self.tbl_singular="Escuela"
