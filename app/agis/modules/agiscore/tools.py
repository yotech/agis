#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for liclipse autocompleting
if False:
    from gluon import *
    from db import *
    from tables import *
    from gluon.contrib.appconfig import AppConfig
    from gluon.tools import Auth, Service, PluginManager
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = DAL('sqlite://storage.sqlite')
    myconf = AppConfig(reload=True)
    auth = Auth(db)
    service = Service()
    plugins = PluginManager()

import os
import cStringIO
import xlsxwriter
from gluon import *
from gluon.sqlhtml import ExportClass
from gluon.contrib.fpdf import FPDF, HTMLMixin
# from gluon.tools import Crud

def tiene_rol_or(roles, user_id=None):
    """
    Retorna True si el usuario actual o user_id tiene alguno de los roles
    """
    auth = current.auth

    if auth.user:
        for rol in roles:
            if auth.has_membership(None, auth.user.id, rol):
                return True
    return False

def tiene_rol(roles, user_id=None, todos=False):
    if not isinstance(roles, (list, tuple)):
        roles = [roles]
    if not len(roles):
        # Si no se especifíca un rol entonces es para todos los roles.
        return True
    if todos:
        return tiene_rol_and(roles, user_id=user_id)

    return tiene_rol_or(roles, user_id=user_id)

def tiene_rol_and(roles, user_id=None):
    """
    Retorna True si el usuario actual o user_id tiene todos los roles
    """
    auth = current.auth
    db = current.db
    u = None
    if user_id:
        u = db.auth_user(user_id)
    else:
        u = auth.user
    if auth.user:
        for rol in roles:
            if not auth.has_membership(None, auth.user.id, rol):
                return False
        return True
    return False

class MyFPDF(FPDF, HTMLMixin):

    def __init__(self):
        super(MyFPDF, self).__init__()
        request = current.request
        font1 = "/{}/static/fonts/{}".format(request.application, 'DejaVuSansCondensed.ttf')
        font2 = "/{}/static/fonts/{}".format(request.application, 'DejaVuSansCondensed-Bold.ttf')
        self.add_font('dejavu', '', font1)
        self.add_font('dejavu', 'B', font2)

    def add_font(self, name, style, path):
        path = self.font_map(path)
        super(MyFPDF, self).add_font(name, style, path, uni=True)

    def font_map(self, path):
        request = current.request
        if path.startswith('/%s/static/' % request.application):
            return os.path.join(request.folder, path.split('/', 2)[2])
        return 'http%s://%s%s' % (request.is_https and 's' or '', request.env.http_host, path)

class CustomExporter(ExportClass):
    label = ''
    file_ext = ''
    content_type = ''
    file_name = ''

    def __init__(self, rows):
        super(CustomExporter, self).__init__(rows)
        request = current.request
        request.vars._export_filename = self.file_name or request.function

class ExporterXLS(CustomExporter):
    label = 'XLS'
    file_ext = "xls"
    content_type = "application/xls"
    file_name = ""

    def __init__(self, rows):
        super(ExporterXLS, self).__init__(rows)
        self.output = cStringIO.StringIO()
        self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True})
        request = current.request
        response = current.response
        request.vars._export_filename = "{}.{}".format(self.file_name, self.file_ext)

class ExporterPDF(CustomExporter):
    label = 'PDF'
    file_ext = "pdf"
    content_type = "application/pdf"

    def __init__(self, rows, orientation=''):
        super(ExporterPDF, self).__init__(rows)
        self.orientation = orientation

    def export(self):
        request = current.request
        response = current.response
        pdf = MyFPDF()
        pdf.alias_nb_pages()
        pdf.add_page(orientation=self.orientation)
        pdf.set_font('dejavu', '', 12)
        filename = '%s/%s.pdf' % (request.controller, request.function)
        if os.path.exists(os.path.join(request.folder, 'views', filename)):
            html = response.render(filename, dict(rows=self.represented()))
        else:
            html = BODY(BEAUTIFY(response._vars)).xml()
        pass
        pdf.write_html(html)
        return XML(pdf.output(dest='S'))

class ExporterPDFLandscape(ExporterPDF):
    def __init__(self, rows):
        super(ExporterPDF, self).__init__(rows)
        self.orientation = 'L'

def split_drop_down(action, elementos):
    response = current.response
    request = current.request
    filename = os.path.join(request.folder, 'views',
                            'split_button_dropdowns.html')
    html = response.render(filename, dict(action=action, elementos=elementos))
    return XML(html)

def inicializar_administrador():
    """Crea el grupo para la administración y el usuario administrador por
    defecto
    """
    db = current.db
    conf = current.conf
    auth = current.auth
    admin_rol = db.auth_group.insert(role=conf.take('roles.admin'))
    admin_user = db.auth_user.insert(
        email="admin@example.com",
        password=db.auth_user.password.validate('admin')[0],
    )
    db.auth_membership.insert(group_id=admin_rol, user_id=admin_user)
    db.commit()
    auth.login_bare('admin@example.com', 'admin')

def inicializar_seguridad():
    """Crea los grupos de seguridad necesarios"""
    db = current.db
    conf = current.conf
    auth = current.auth
    inicializar_administrador()
    db.auth_group.insert(role=conf.take('roles.profesor'))
    db.auth_group.insert(role=conf.take('roles.oexamen'))
    db.auth_group.insert(role=conf.take('roles.cinscrip'))
    db.auth_group.insert(role=conf.take('roles.incribidor'))

def probar_base_de_datos():
    """Retorna True si la base de datos ya esta inicializada"""
    db = current.db
    if db(db.auth_user.id > 0).count() > 0:
        return True
    # en cc retornar Falso
    return False

def selector(consulta, campos, var_name, tabla=None):
    """Define un GRID que puede ser utilizado para seleccionar uno de sus
    elementos que es entonces pasado como parametro en el query string a el
    cotrolador/funcion especificado.

    consulta: query a ejecutar
    campos: campos a mostrar en el grid
    var_name: nombre a utilizar para generar el parametro ID del enlace de
              selección
    tabla: si es diferente de None se usa para seleccionar la tabla de
                donde se extrae el ID
    """
    def enlaces(fila):
        request = current.request
        T = current.T
        parametros = request.vars
        # limpiar busquedas anterirores y otros parametros introducidos
        # por SQLFORM.grid
        if request.vars.keywords:
            request.vars.keywords = ''
        if request.vars.order:
            request.vars.order = ''
        if not tabla:
            parametros[var_name] = fila.id
        else:
            parametros[var_name] = fila[tabla].id
        return A(SPAN('', _class='glyphicon glyphicon-hand-up'),
                 _class="btn btn-default", _title=T("Seleccionar"),
                 _href=URL(c=request.controller, f=request.function,
                           vars=parametros, args=request.args))
    enlaces = [dict(header='', body=enlaces)]
    return manejo_simple(consulta, enlaces=enlaces,
                         campos=campos, crear=False,
                         borrar=False, editable=False,
                         buscar=True,)

def manejo_simple(conjunto,
        orden=[], longitud_texto=100, editable=True, enlaces=[], buscar=False,
        campos=None, crear=True, borrar=True, csv=False, exportadores={},
        detalles=False
        ):
    manejo = SQLFORM.grid(query=conjunto,
        details=detalles,
        csv=csv,
        fields=campos,
        searchable=buscar,
        create=crear,
        deletable=borrar,
        editable=editable,
        showbuttontext=False,
        links=enlaces,
        exportclasses=exportadores,
        maxtextlength=longitud_texto,
        orderby=orden,
    )
    return manejo

def inicializar_base_datos():
    db = current.db
    request = current.request
    # academic regions
    db.region_academica.import_from_csv_file(
        open(os.path.join(request.folder, 'db_region_academica.csv'), 'r')
    )
    db.commit()
    paises_list = os.path.join(request.folder, 'db_pais.csv')
    if os.path.exists(paises_list):
        db.pais.import_from_csv_file(open(paises_list, 'r'))
        db.commit()
    db.provincia.import_from_csv_file(
        open(os.path.join(request.folder, 'db_provincia.csv'), 'r')
    )
    db.commit()
    region = db.region_academica[1]
    escuela = db.escuela.insert(nombre='IES EXEMPLO',
        region_academica_id=region.id,
        clasificacion='10',
        naturaleza='1',
        codigo_registro='000',
        codigo='07101000'
    )
    db.commit()
    # regímenes
    db.regimen.import_from_csv_file(
        open(os.path.join(request.folder, 'db_regime.csv'), 'r')
    )
    db.commit()
    tmp_prov = db.provincia[1]
    unidad_organica_id = db.unidad_organica.insert(nombre='SEDE CENTRAL (DEFECTO)',
        provincia_id=tmp_prov.id,
        nivel_agregacion='1',
        clasificacion='20',
        codigo_registro='000',
        codigo_escuela='00',
        escuela_id=escuela
    )
    db.commit()
    db.descripcion_carrera.import_from_csv_file(
        open(os.path.join(request.folder, 'careers_des.csv'), 'r')
    )
    db.commit()
    # municipios
    db.municipio.import_from_csv_file(
        open(os.path.join(request.folder, 'db_municipality.csv'), 'r')
    )
    db.commit()
    # comunas
    db.comuna.import_from_csv_file(
        open(os.path.join(request.folder, 'db_commune.csv'), 'r')
    )
    db.commit()
    # tipos de enseñanza media
    db.tipo_escuela_media.import_from_csv_file(
        open(os.path.join(request.folder, 'db_middle_school_type.csv'), 'r')
    )
    db.commit()
    db.tipo_documento_identidad.bulk_insert([
       {'nombre': 'BILHETE DE IDENTIDADE'},
       {'nombre': 'PASSAPORTE'},
    ])
    db.commit()
    # tipos de discapacidad
    db.discapacidad.import_from_csv_file(
       open(os.path.join(request.folder, 'db_special_education.csv'), 'r')
    )
    db.commit()
    # tipos de pago, emolumentos
    from agiscore.db import tipo_pago
    tipo_pago.definir_tabla()
    db.tipo_pago.import_from_csv_file(
        open(os.path.join(request.folder, 'db_tipo_pago.csv'), 'r')
    )
    from agiscore.db import ano_academico
    nombre = ano_academico.ano_actual()
    a_id = db.ano_academico.insert(nombre=nombre,
                                   unidad_organica_id=unidad_organica_id)
    from agiscore.db import evento
    evento.crear_eventos(db, a_id)
    db.commit()

requerido = [IS_NOT_EMPTY(error_message=current.T('Información requerida'))]
