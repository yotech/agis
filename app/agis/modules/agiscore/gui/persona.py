# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from agiscore.gui.mic import *
from agiscore.db import persona as model
from agiscore.db import pais as pais_model
from agiscore.validators import IS_DATE_LT
import datetime

__doc__ = """Herramientas y componentes para el manejo personas"""

def leyenda_persona():
    """Retorna componente para usar como leyenda en listados de personas
    """
    T = current.T
    l = Leyenda()
    l.append(T('Género'), model.PERSONA_GENERO_VALUES)
    l.append(T('Estado Civil'), model.PERSONA_ESTADO_CIVIL_VALUES)
    l.append(T('Estado Político'), model.PERSONA_ESTADO_POLITICO_VALUES)
    return l

def form_crear_persona():
    """
    Crea un formulario para la entrada de los datos de una persona.

    Retorna una tupla con el formulario y los datos entrados:

    (form, data)

    Si data es None entonces no se han entrado correctamente los datos y es
    necesario llamar de nuevo a esa funsión
    """
    session = current.session
    T = current.T
    model.definir_tabla()
    db = current.db
    request = current.request
    mi_vars = Storage(request.vars)  # make a copy
    mi_vars._form_crear_persona = 1
    cancelar = URL(c=request.controller, f=request.function, args=request.args, vars=mi_vars)
    if request.vars._form_crear_persona:
        session.form_crear_persona = None
        request.vars._form_crear_persona = None
        redirect(URL(c=request.controller, f=request.function))
    if session.form_crear_persona is None:
        session.form_crear_persona = Storage(dict(step=0))
        session.form_crear_persona.valores = Storage(dict())
    data = session.form_crear_persona.valores
    step = session.form_crear_persona.step

    if step == 0:
        # datos personales
        fld_nombre = db.persona.get("nombre")
        fld_apellido1 = db.persona.get("apellido1")
        fld_apellido2 = db.persona.get("apellido2")
        fld_fecha_nacimiento = db.persona.get("fecha_nacimiento")
        fld_genero = db.persona.get("genero")
        fld_padre = db.persona.get("nombre_padre")
        fld_madre = db.persona.get("nombre_madre")
        fld_estado_civil = db.persona.get("estado_civil")
        fld_estado_politico = db.persona.get("estado_politico")
        fld_pais_origen = db.persona.get("pais_origen")

        fld_nombre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_apellido1.requires = IS_UPPER()
        fld_apellido2.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        hoy = datetime.date.today()
        _15anos = datetime.timedelta(days=(15*365))
        fld_fecha_nacimiento.requires = [IS_DATE_LT(maximo=hoy-_15anos),
                                         IS_NOT_EMPTY()]
        fld_padre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_madre.requires = [IS_NOT_EMPTY(), IS_UPPER()]
        fld_pais_origen.default = 3
        fld_pais_origen.requires = IS_IN_DB(db, "pais.id", "%(nombre)s", zero=None)
        
        form = SQLFORM.factory(fld_nombre,
            fld_apellido1,
            fld_apellido2,
            fld_fecha_nacimiento,
            fld_genero,
            fld_padre, fld_madre,
            fld_estado_civil,
            fld_estado_politico,
            fld_pais_origen,
            table_name="persona",
            submit_button=T("Next"),
            )
        form.add_button("Cancel", cancelar)
        title = DIV(H3(T("Datos personales"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process().accepted:
            session.form_crear_persona.step = 1
            # en form_crear_persona.valores tenemos los datos validados
            session.form_crear_persona.valores.update(form.vars)
            redirect(URL(request.controller, request.function))
        return (c, None)

    if step == 1:
        # ORIGEN
        # Si el país de origen es ANGOLA, se puede preguntar por el lugar
        # de nacimiento.
        origen = db.pais(int(data.pais_origen))
        campos = list()
        if origen.codigo == pais_model.ANGOLA:
            s = db(db.comuna.id > 0 and db.municipio.id == db.comuna.municipio_id)
            comunas = [(r.comuna.id, "{0} / {1}".format(r.comuna.nombre, r.municipio.nombre)) \
                for r in s.select(orderby=db.comuna.nombre)]
            fld_lugar_nacimiento = db.persona.get("lugar_nacimiento")
            fld_lugar_nacimiento.requires = IS_IN_SET(comunas, zero=None)
            # -- arreglo para la representasión de las comunas.
            campos.append(fld_lugar_nacimiento)
        else:
            fld_tiene_nacionalidad = Field('tiene_nacionalidad', 'boolean', default=True)
            fld_tiene_nacionalidad.label = T("¿Posee nacionalidad angolana?")
            campos.append(fld_tiene_nacionalidad)
        form = SQLFORM.factory(*campos, table_name="persona", submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        title = DIV(H3(T("Origen"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process().accepted:
            session.form_crear_persona.valores.update(form.vars)
            session.form_crear_persona.step = 2
            redirect(URL(request.controller, request.function))
        return (c, None)
    
    if data.lugar_nacimiento or data.tiene_nacionalidad:
        # BILHETE DE IDENTIDADE
        session.form_crear_persona.valores.tipo_documento_identidad_id = 1
    else:
        # PASAPORTE
        session.form_crear_persona.valores.tipo_documento_identidad_id = 2
        
    if step == 2:
        # residencia 1
        campos = list()
        fld_numero_identidad = db.persona.get("numero_identidad")
        fld_pais_residencia = db.persona.get("pais_residencia")
        fld_pais_residencia.requires = IS_IN_DB(db, "pais.id", "%(nombre)s", zero=None)
        if data.tipo_documento_identidad_id == 1:
            fld_pais_residencia.default = 3
            fld_numero_identidad.label = T("Carnet de identidad")
        else:
            fld_pais_residencia.default = data.pais_origen
            fld_numero_identidad.label = T("Número de pasaporte")
        fld_numero_identidad.requires = [IS_NOT_EMPTY(), IS_UPPER(),
            IS_NOT_IN_DB(db, "persona.numero_identidad")]
        campos.append(fld_numero_identidad)
        campos.append(fld_pais_residencia)
        form = SQLFORM.factory(*campos, table_name="persona", submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        title = DIV(H3(T("Residencia 1/2"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process().accepted:
            session.form_crear_persona.valores.update(form.vars)
            session.form_crear_persona.step = 3
            redirect(URL(request.controller, request.function))
        return (c, None)

    if step == 3:
        # residencia 2
        campos = list()
        fld_direccion = db.persona.get("direccion")
        if data.pais_residencia == '3':
            fld_comuna = db.persona.get("dir_comuna_id")
            fld_comuna.label = T("Localidad")
            s = db(db.comuna.id > 0 and db.municipio.id == db.comuna.municipio_id)
            comunas = [(r.comuna.id, "{0} / {1}".format(r.comuna.nombre, r.municipio.nombre)) \
                for r in s.select(orderby=db.comuna.nombre)]
            fld_comuna.requires = IS_IN_SET(comunas, zero=None)
            campos.append(fld_comuna)
        campos.append(fld_direccion)
        form = SQLFORM.factory(*campos, table_name="persona", submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        title = DIV(H3(T("Residencia 2/2"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process().accepted:
            session.form_crear_persona.valores.update(form.vars)
            session.form_crear_persona.step = 4
            redirect(URL(request.controller, request.function))
        return (c, None)

    if step == 4:
        # datos de contacto
        campos = list()
        fld_telefono = db.persona.get("telefono")
        fld_telefono2 = db.persona.get("telefono_alternativo")
        fld_email = db.persona.get("email")
        fld_email.requires = IS_EMPTY_OR(IS_EMAIL())
        fld_email2 = Field('email2', 'string', length=50)
        fld_email2.label = T("Confirmar E-mail")
        fld_email2.requires = IS_EMPTY_OR(
                IS_EQUAL_TO(request.vars.email))
        if request.vars.email:
            fld_email2.requires = IS_EQUAL_TO(request.vars.email)
        campos.append(fld_telefono)
        campos.append(fld_telefono2)
        campos.append(fld_email)
        campos.append(fld_email2)
        form = SQLFORM.factory(*campos, table_name="persona", submit_button=T("Next"))
        form.add_button("Cancel", cancelar)
        title = DIV(H3(T("Contacto"), _class="panel-title"),
            _class="panel-heading")
        c = DIV(title, DIV(form, _class="panel-body"),
                   _class="panel panel-default")
        if form.process().accepted:
            session.form_crear_persona.valores.telefono = form.vars.telefono
            session.form_crear_persona.valores.telefono_alternativo = form.vars.telefono_alternativo
            session.form_crear_persona.valores.email = form.vars.email
            session.form_crear_persona.step = 5
            redirect(URL(request.controller, request.function))
        return (c, None)

    data.pais_origen = int(data.pais_origen)
    data.pais_residencia = int(data.pais_residencia)
    if data.lugar_nacimiento:
       data.lugar_nacimiento = int(data.lugar_nacimiento)
    if data.dir_comuna_id:
        data.dir_comuna_id = int(data.dir_comuna_id)
    session.form_crear_persona = None
    return ("OK", data)

def form_editar(uuid):
    """Dado el UUID de una persona retorna el formulario correspondiente para
    la edición de los datos de la misma"""
    model.definir_tabla()
    db = current.db
    T = current.T
    request = current.request
    p = model.obtener_por_uuid(uuid)
    title = H3(T("Datos personales"))
    if request.vars.email:
        db.persona.email.requires.append(IS_EMAIL())
        db.persona.email.requires.append(
            IS_NOT_IN_DB(db, 'persona.email'))
    f = SQLFORM(db.persona, p)
    c = CAT(title, DIV(DIV(f, _class="panel-body"),
               _class="panel panel-default"))
    return (c, f)
