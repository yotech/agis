#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from agiscore.db import persona

DOCUMENTOS_VALUES = {
    '1':'CERTIFICADO ORIGINAL',
    '2':'CÓPIA DE DOCUMENTO',
    '3':'DOCUMENTO DE TRABALHO',
    '4':'DOCUMENTO MILITAR',
    '5':'INTERNADO',
}
def documentos_represent(valores, fila):
    res = ""
    if valores is None:
        return ""
    for i in valores:
        if res == "":
            res += DOCUMENTOS_VALUES[ i ]
        else:
            res += ", " + DOCUMENTOS_VALUES[ i ]
    return res

FORMA_ACCESO_VALUES = {
    '01': 'EXAME DE INGRESSO',
    '02': 'GRADUADO UNIVERSITARIO',
    '03': 'OUTRA',
    '04': 'CONCURSO ACADEMICO'
}
FA_EXAME_DE_INGRESSO = '01'

MODALIDAD_VALUES = {
    '1': 'ENSINO PRESENCIAL',
    '2': 'SEMI-PRESENCIAL',
    '3': 'A DISTANCIA',
}

TRAB_TIPO_INSTITUTO = {
    '1': 'PÚBLICO',
    '2': 'PRIVADO'
}

BOLSA_ESTUDIOS_VALUES ={
    'A': 'Aproveitamento academico-referencia',
    'B': 'Careccia de recurso do agregado familiar',
    'C': 'Comportamento Exemplar do estudante',
    'D': 'Idade regilamente frequentar o superior',
    'E': 'Bolsa externa',
    'G': 'Bolsa de Credito Interno',
    'H': 'Bolsero de Institucion (funcionario)',
    'N': 'Sim bolsa'
}

TRAB_TITULO_VALUES = {
    '1': 'BACHARELATO',
    '2': 'LICENCIATURA',
    '3': 'LICENCIATURA BIETÁPICA'
}

def estudiante_format(registro):
    db = current.db
    definir_tabla()
    return db.persona[registro.persona_id].nombre_completo

def obtener_por_persona(persona_id):
    db = current.db
    definir_tabla()
    p = db.persona(persona_id)
    if not p:
        return None
    return p.estudiante.select().first()

def esconder_campos():
    visibilidad(False)
def mostrar_campos():
    visibilidad(True)

def visibilidad(valor):
    """Cambia la propiedad readable de todos los campos de estudiante"""
    db = current.db
    definir_tabla()
    for f in db.estudiante:
        f.readable = False

def obtener_persona(estudiante_id):
    """Dado un ID de estudiante retorna el registro de la persona asociada"""
    db = current.db
    definir_tabla()
    est = db.estudiante[estudiante_id]
    return db.persona[est.persona_id]

def copia_uuid_callback(valores):
    """Se llama antes de insertar un valor en la tabla

    En este caso lo estamos usando para copiar el UUID de la persona
    """
    db = current.db
    p = db.persona(valores['persona_id'])
    valores['uuid'] = p.uuid

def definir_tabla():
    db = current.db
    T = current.T
    persona.definir_tabla()
    if not hasattr(db, 'estudiante'):
        tbl = db.define_table('estudiante',
            Field('persona_id', 'reference persona'),
            Field('es_trabajador', 'boolean', default = True),
            # -- datos laborales
            Field('trab_profesion', 'string', length=30),
            Field('trab_nombre', 'string', length=30),
            Field('trab_provincia', 'reference provincia'),
            Field('trab_tipo_instituto', 'string', length=1),
            Field('trab_titulo', 'string', length=1),
            # -- procedencia
            Field('pro_habilitacion', 'string', length=3),
            Field('pro_tipo_escuela', 'reference tipo_escuela_media'),
            Field('pro_escuela_id', 'reference escuela_media'),
            Field('pro_carrera', 'string', length=180),
            Field('pro_ano', 'string', length=4),
            Field('pro_media', 'float'),
            # -- otros
            Field('discapacidades', 'list:reference discapacidad'),
            Field('documentos', 'list:string'),
            Field('forma_acceso', 'string', length=2),
            Field('modalidad', 'string', length=1),
            Field('es_internado', 'boolean', default=False),
            Field('ano_ies', 'string', length=4),
            Field('ano_es', 'string', length=4),
            Field('media_acceso', 'float', default=0.0),
            Field('bolsa_estudio', 'string', length=1, default='N'),
            Field('codigo', 'string', length=12, default=''),
            Field('unidad_organica_id', 'reference  unidad_organica'),
            db.my_signature,
            format=estudiante_format,
            )
        tbl._before_insert.append(copia_uuid_callback)
        
        # campos: información laboral
        tbl.trab_profesion.label = T("Profesión")
        tbl.trab_profesion.comment = T('Nombre de la profesión que realiza')
        tbl.trab_nombre.label = T("Trabajo/Cargo")
        tbl.trab_nombre.comment = T('Nombre del trabajo o cargo que ocupa')
        tbl.trab_provincia.default = None
        tbl.trab_provincia.label = T("Provincia/Trabajo")
        tbl.trab_tipo_instituto.label = T("Tipo de institución")
        tbl.trab_tipo_instituto.represent = lambda v,f: 'N/D' if v is None \
                                                else TRAB_TIPO_INSTITUTO[v]
        tbl.trab_titulo.label = T("Titulo (Trabajo)")
        tbl.trab_titulo.comment = T('''
            Tipo de titulo que otorga el centro laboral
        ''')
        #--
        tbl.pro_habilitacion.label = T("Habilitación")
        tbl.pro_habilitacion.requires = IS_IN_SET(["12ª", "13ª"], zero=None)
        tbl.pro_tipo_escuela.label = T('Tipo de enseñanza media')
        tbl.pro_tipo_escuela.requires = IS_IN_DB(db,
                                                 'tipo_escuela_media.id',
                                                 '%(nombre)s', zero=None)
        tbl.pro_carrera.label = T("Carrera (procedencia)")
        tbl.pro_carrera.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        tbl.pro_ano.label = T('Año de conclusión')
        tbl.pro_ano.requires = IS_INT_IN_RANGE(1900, 3000)
        tbl.pro_escuela_id.label = T("Centro enseñanza media")
        tbl.pro_media.label = T("Promedio alcanzado")
        tbl.pro_media.requires = [IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0.0, 100.0)]
        # -- años de matricula
        tbl.ano_ies.label = T('Año de matricula (IES)')
        tbl.ano_es.label = T('Año de matricula (ES)')
        tbl.ano_ies.requires = IS_INT_IN_RANGE(1900, 3000)
        tbl.ano_es.requires = IS_INT_IN_RANGE(1900, 3000)
        
        tbl.discapacidades.label = T('Educación especial')
        tbl.discapacidades.default = [5]
        tbl.documentos.requires = IS_IN_SET(DOCUMENTOS_VALUES,
                                            multiple=True)
        tbl.documentos.represent = documentos_represent
        tbl.documentos.label = T('Documentos')
        
        # -- forma de acceso a la enseñanza superior
        tbl.forma_acceso.label = T("Forma de acceso")
        tbl.forma_acceso.requires = IS_IN_SET(FORMA_ACCESO_VALUES,
                                              zero=None)
        tbl.forma_acceso.represent = lambda v,f: FORMA_ACCESO_VALUES[v]

        # -- modalidad de enseñánza
        tbl.modalidad.label = T('Modalidad de enseñanza')
        tbl.modalidad.requires = IS_IN_SET(MODALIDAD_VALUES, zero=None)
        tbl.modalidad.represent = lambda v,f: MODALIDAD_VALUES[v]
        tbl.modalidad.default = '1'
        
        #-- ¿es internado?
        tbl.es_internado.label = T("¿Es internado?")
        
        #-- bolsa de estudios
        tbl.bolsa_estudio.label = T("Bolsa de estudio")
        tbl.bolsa_estudio.requires = IS_IN_SET(BOLSA_ESTUDIOS_VALUES, zero=None)
        tbl.bolsa_estudio.represent = lambda v,f: BOLSA_ESTUDIOS_VALUES[v]
        tbl.codigo.label = T("Mecanográfico")
        
        # -- media en examenes de acceso
        tbl.media_acceso.label = T("Media/Acceso")
        tbl.media_acceso.comment = T("""
        Media obtenida en los examenes de acceso
        """)
        tbl.media_acceso.writable = False
