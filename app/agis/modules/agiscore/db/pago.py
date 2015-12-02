#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import persona
from agiscore.db import candidatura
from agiscore.db import tipo_pago
from agiscore.tools import ExporterXLS


class PagoInscripcionXLS(ExporterXLS):
    file_name = "Reporte de pagos - INSCRIPCIÓN"
    
    def __init__(self, *args, **kawrgs):
        super(PagoInscripcionXLS, self).__init__(*args, **kawrgs)
    
    def export(self):
        db = current.db
        T = current.T
        hoja = self.workbook.add_worksheet()
        wb = self.workbook
        records = self.represented()
        # primera persona en el listado
        _per = db.persona(records[0][0])
        # de aquí podemos sacar la escuela/UO/otros datos
        _est = db.estudiante(persona_id=_per.id)
        _can = db.candidatura(estudiante_id=_est.id)
        _aa = db.ano_academico(_can.ano_academico_id)
        _uo = db.unidad_organica(_can.unidad_organica_id)
        _esc = db.escuela(_uo.escuela_id)
        concepto = db(
            db.tipo_pago.nombre == "INSCRIÇÃO AO EXAME DE ACESSO"
        ).select().first()
        neg = wb.add_format({'bold': True}) 
        
        # nombre de la escuela
        hoja.merge_range('A1:K1', _esc.nombre.decode('utf-8'), neg)
        hoja.merge_range('A2:K2', _uo.nombre.decode('utf-8'), neg)
        hoja.merge_range('A4:F4',
                         T("Registro de pagos por INSCRIPCIÓN").decode('utf-8'))
        ano_a = T("Año académico: {}".format(_aa.nombre))
        hoja.merge_range('A5:F5', ano_a.decode('utf-8'))
        hoja.write('A8', '#', wb.add_format({'bold': True, 'align': 'right'}))
        hoja.set_column('B:B', 30)
        hoja.write('B8', T("Nombre").decode("utf-8"),
                   wb.add_format({'bold': True, 'align': 'left'}))
        hoja.set_column('C:C', 15)
        hoja.write('C8', T("Avonado").decode('utf-8'),
                   wb.add_format({'bold': True, 'align': 'right'}))
        hoja.set_column('D:D', 15)
        hoja.write('D8', T("Estado").decode('utf-8'),
                   wb.add_format({'bold': True, 'align': 'left'}))
        fila = 0
        total = 0
        for fila, r in enumerate(records):
            _per = db.persona(r[0])
            _est = db.estudiante(persona_id=_per.id)
            _can = db.candidatura(estudiante_id=_est.id)
            ni = _can.numero_inscripcion or 'N/D'
            hoja.write(fila+8, 0,
                       ni,
                       wb.add_format({'align': 'right'}))
            hoja.write(fila+8, 1, _per.nombre_completo.decode('utf-8'),
                       wb.add_format({'align': 'left'}))
            format1 = wb.add_format()
            format1.set_num_format("$#,##0.00")
            cantidad = cantidad_avonada(_per, concepto)
            total += cantidad
            hoja.write(fila+8, 2, cantidad, format1)
            estado = T('CON DEUDAS')
            if _can.estado_candidatura in [candidatura.ADMITIDO,
                                           candidatura.INSCRITO,
                                           candidatura.NO_ADMITIDO]:
                estado = T('INSCRITO')
            hoja.write(fila+8, 3, estado.decode('utf-8'))
        inscritos = ((db.candidatura.estado_candidatura == candidatura.INSCRITO) |
                     (db.candidatura.estado_candidatura == candidatura.NO_ADMITIDO) |
                     (db.candidatura.estado_candidatura == candidatura.ADMITIDO))
        con_deuda = (db.candidatura.estado_candidatura == candidatura.INSCRITO_CON_DEUDAS)
        
        cantidad_incritos = candidatura.contar_candidatos(
            ano_academico_id=_aa.id,
            condicion=inscritos)
        cantidad_deuda = candidatura.contar_candidatos(
            ano_academico_id=_aa.id,
            condicion=con_deuda)
        format1 = wb.add_format()
        format1.set_num_format("#,##0")
        hoja.write(fila+10, 1,
                   T("Inscriptos").decode('utf8'),
                   wb.add_format({'bold': True, 'align': 'right'}))
        hoja.write(fila+10, 2, cantidad_incritos, format1)
        hoja.write(fila+11, 1,
                   T("Con deuda").decode('utf8'),
                   wb.add_format({'bold': True, 'align': 'right'}))
        hoja.write(fila+11, 2, cantidad_deuda, format1)
        format1 = wb.add_format()
        format1.set_num_format("$#,##0.00")
        hoja.write(fila+12, 1,
                   T("Recaudado").decode('utf8'),
                   wb.add_format({'bold': True, 'align': 'right'}))
        hoja.write_formula(fila + 12, 2,
                           "=SUM(C{}:C{})".format(9, fila+9),
                           format1,
                           value=total)
        wb.close()
        return self.output.getvalue()

FORMA_PAGO_VALORES={
    '1':'BANCO',
    '2':'TARGETA'
}
def forma_pago_represent(valor, fila):
    T=current.T
    return T( FORMA_PAGO_VALORES[valor] )

def cantidad_avonada(persona, concepto):
    """Dado el id de una persona calcula la suma total de sus pago dado un
    concepto
    """
    db = current.db
    sum = db.pago.cantidad.sum()
    query = (db.pago.persona_id == persona.id)
    query &= (db.pago.tipo_pago_id == concepto.id)
    total = db(query).select(sum).first()[sum]
    if total is None:
        total = 0.0
        
    return total

def definir_tabla():
    db=current.db
    T=current.T
    persona.definir_tabla()
    tipo_pago.definir_tabla()
    if not hasattr( db, 'pago' ):
        db.define_table( 'pago',
            Field( 'persona_id','reference persona' ),
            Field( 'tipo_pago_id','reference tipo_pago' ),
            Field( 'forma_pago','string',length=1 ),
            Field( 'numero_transaccion','string',length=20 ),
            Field( 'cantidad','double' ),
            Field( 'codigo_recivo','string',length=10 ),
            )
        db.pago.forma_pago.label=T( 'Forma de pago' )
        db.pago.forma_pago.requires = IS_IN_SET( FORMA_PAGO_VALORES,zero=None )
        db.pago.forma_pago.represent=forma_pago_represent
        db.pago.numero_transaccion.label=T( 'Número de transacción' )
        db.pago.numero_transaccion.requires= [IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) )]
        db.pago.numero_transaccion.requires.append(
            IS_NOT_IN_DB(db, 'pago.numero_transaccion')
            )
        db.pago.persona_id.label=T( 'Avona' )
        db.pago.tipo_pago_id.label=T( 'Tipo de pago' )
        db.pago.cantidad.label=T( 'Cantidad' )
        db.pago.cantidad.requires.append( IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) ) )
        db.pago.codigo_recivo.label=T( 'Código recivo' )
        db.pago.codigo_recivo.requires=[IS_NOT_EMPTY( error_message=current.T( 'Información requerida' ) )]
        db.pago.codigo_recivo.requires.append(
            IS_NOT_IN_DB(db, 'pago.codigo_recivo')
            )
        db.commit()
