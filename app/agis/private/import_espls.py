#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
import MySQLdb

# CONFIGURACION
espls_host = "192.168.40.2"
espls_user = "espls"
espls_pass = "espls"
espls_db = "espls"


ESTADO_CIVIL = {
    1: 'C',
    2: 'S',
    3: 'D',
    4: 'O'
}
TIPO_DOC = {
    u'Bilhete de Identidade': 1,
    u'Passaporte': 2,
    u'Carta de Condição': 1,
}
ESTO_POLITICO = {
    u'Civil': 'C', 
    u'Polícia': 'P',
    u'Militar': 'M',
}
HABILITACION = {
    u'Outra': "12ª",
    u'13ª': "13ª",
    u'12ª': "12ª",
    u'11ª': "12ª"
}
CARRERAS = {
    3: 11,
    2: 4,
    12: 9,
    9: 10,
    5: 2,
    14: 6,
    4: 3,
    13: 8,
    6: 1,
    10: 5
}

dbespls = MySQLdb.connect(host=espls_host,
                          user=espls_user,
                          passwd=espls_pass,
                          db=espls_db)

# importar las especialidades
sub_q = """
SELECT * FROM espls.uo_especialidades;
"""
c2 = dbespls.cursor()
c2.execute(sub_q)
ESPECIALIDADES = dict()
for r in c2:
    esp_data = Storage()
    esp_data.nombre = r[2].decode('latin1').strip().upper()
    esp_data.abreviatura = r[1].decode('latin1').strip().upper()
    esp_data.carrera_id = 4
    tbl = current.db.especialidad
    especialidad_id = tbl.insert(**tbl._filter_fields(esp_data))
    ESPECIALIDADES[r[0]] = especialidad_id
print ESPECIALIDADES
c2.close()


query = """
SELECT * FROM espls.pessoas as p, espls.estudantes as e 
WHERE p.idpessoa = e.idtabestudante and p.tipopessoa = 'Estudante';
"""

cursor = dbespls.cursor()
cursor.execute(query)

for result in cursor:
    pdata = Storage()  # datos personales
    pdata.nombre = (result[7].decode('latin1')).strip()
    if result[8] != '':
        pdata.apellido1 = (result[8].decode('latin1')).strip()  
    pdata.apellido2 = (result[9].decode('latin1')).strip().upper()
    pdata.fecha_nacimiento = result[12]
    pdata.genero = 'M' if result[16] == 1 else 'F'
    pdata.nombre_madre = (result[21].decode('latin1')).strip().upper()
    pdata.nombre_padre = (result[20].decode('latin1')).strip().upper()
    pdata.estado_civil = ESTADO_CIVIL[result[18]]
    pdata.tipo_documento_identidad_id = TIPO_DOC[result[22].decode('latin1')] 
    pdata.numero_identidad = result[23].strip()
    pdata.estado_politico = ESTO_POLITICO[result[43].decode('latin1')]
    pdata.pais_residencia = 3
        
    tbl = current.db.persona
    persona_id = tbl.insert(**tbl._filter_fields(pdata))
    est_data = Storage()
    est_data.persona_id = persona_id
    est_data.es_trabajador = True if result[44] == 1 else False
    if est_data.es_trabajador:
        est_data.trab_profesion = (result[46].decode('latin1')).strip().upper()
    # pro_habilitacion
    est_data.pro_habilitacion = HABILITACION[result[38].decode('latin1')]
    est_data.pro_carrera = (result[41].decode('latin1')).strip().upper()
    est_data.pro_ano = str(result[42])
    est_data.pro_media = 0.0
    est_data.forma_acceso = '01'
    est_data.es_internado = False
    est_data.modalidad = '1'
    est_data.unidad_organica_id = 1
    est_data.codigo = result[37] # ver aquí si se puede calcular
    if result[37]:
        est_data.ano_ies = "20{}{}".format(est_data.codigo[4],
                                           est_data.codigo[5])
        est_data.ano_es = est_data.ano_ies
    tbl = current.db.estudiante
    estudiante_id = tbl.insert(**tbl._filter_fields(est_data))
    
    # matricula
    ma_data = Storage()
    ma_data.estudiante_id = estudiante_id
    ma_data.ano_academico_id = 1
    # obtener el nivel
    idEstudante = result[36]
    sub_q = """
    SELECT idnivel FROM espls.estudantes WHERE idEstudante = %s
    """
    c2 = dbespls.cursor()
    c2.execute(sub_q, idEstudante)
    niv = c2.fetchone()
    ma_data.nivel = niv[0] if niv[0] != 6 else 7
    c2.close()
    ma_data.situacion = '2'
    ma_data.estado_uo = '1'
    ma_data.regimen_id = 1 if result[57] in [1, 3] else 2
    if result[63] in [5, 6]:
        ma_data.espacialidad_id = ESPECIALIDADES[result[63]]
    ma_data.carrera_id = CARRERAS[result[58]]
    tbl = current.db.matricula
    tbl.insert(**tbl._filter_fields(ma_data))

current.db.commit()
cursor.close()
dbespls.close()
