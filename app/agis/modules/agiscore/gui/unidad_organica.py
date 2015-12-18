# -*- coding: utf-8 -*-
from gluon import current
from gluon import redirect, URL, CAT, DIV, SPAN
from agiscore import tools
from agiscore.db import unidad_organica as uo_model
from agiscore.db import escuela as escuela_model
from agiscore.gui.mic import grid_simple, Accion

__doc__ = """Herramientas de GUI para eventos"""

def manejo_unidades(escuela, db, T, request=None, auth=None, conf=None):
    if auth is None:
        auth = current.auth
    if conf is None:
        conf = current.conf
    if request is None:
        request = current.request
    editar = auth.has_membership(role=conf.take('roles.admin'))
    crear = auth.has_membership(role=conf.take('roles.admin'))
    deletable = auth.has_membership(role=conf.take('roles.admin'))
    query = (db.unidad_organica.id > 0)
    query &= (db.unidad_organica.escuela_id == escuela.id)
    campos = [db.unidad_organica.id,
              db.unidad_organica.nombre]
    
    if 'new' in request.args:
        db.unidad_organica.escuela_id.default = escuela.id
        db.unidad_organica.escuela_id.writable = False
    
    if 'edit' in request.args:
        db.unidad_organica.escuela_id.writable = False
    
    db.unidad_organica.id.readable = False
    
    
    # antes de crear el grid añadir los links de acceso al resto de los modulos
    def _enlaces(row):
        a = Accion(CAT(SPAN('', _class='glyphicon glyphicon-hand-up'),
                       ' ', T('Acceder')),
            URL('unidad', 'index', args=[row.id]),
            True,
            _class="btn btn-success",
            _title=T("Acceder a los componentes de la Unidad")
            )
        
        return a
    
    enlaces = [dict(header='', body=_enlaces)]
    if 'edit' in request.args or 'new' in request.args: 
        enlaces = []
    
    return grid_simple(query,
                       orderby=[db.unidad_organica.nombre],
                       fields=campos,
                       maxtextlength=100,
                       editable=editar,
                       create=crear,
                       searchable=False,
                       links=enlaces,
                       deletable=deletable)

def uo_para_persona(p):
    """dado un record de persona buscar a cual unidad organica pertenece segun
    el tipo de persona y retorna el id de la UO
    """
    db = current.db
    est = p.estudiante.select().first()
    pro = p.profesor.select().first()
    if est:
        # TODO: ver como se hace para los estudiantes
        print est
    if pro:
        dpto = db.departamento(pro.departamento_id)
        return dpto.unidad_organica_id
    return None

def seleccionar_uo():
    """
    Retorna un grid por medio del cual se puede seleccionar una unidad organica
    el valor del ID seleccionado quedará en:

        request.vars.unidad_organica_id

    el grid para la selección se puede obtener por medio de:

        context.manejo
    """
    uo_model.definir_tabla()
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    auth = current.auth
    per = db.auth_user(auth.user.id).persona.select().first()
    if per and uo_para_persona(per):
        # seleccionar la primera y redirecionar a la vista que nos llamo
        if request.vars.keywords:
            request.vars.keywords = ''
        if request.vars.order:
            request.vars.order = ''
        parametros = request.vars
        args = request.args
        parametros.unidad_organica_id = uo_para_persona(per)
        u = URL(c=request.controller, f=request.function,
                     vars=parametros, args=args)
        redirect(u)  # return's via exceptions
    if db(uo_model.conjunto()).count() > 1:
        # Si hay más de una UO
        co = CAT()
        header = DIV(T("Seleccionar Unidad Orgánica"), _class="panel-heading")
        body = DIV(_class="panel-body")
        panel = DIV(header, body, _class="panel panel-default")
        # preparar el los campos del grid
        for f in db.unidad_organica:
            f.readable = False
        db.unidad_organica.codigo.readable = True
        db.unidad_organica.nombre.readable = True
        grid = tools.selector(uo_model.conjunto(),
                [db.unidad_organica.codigo,
                 db.unidad_organica.nombre],
                'unidad_organica_id',
            )
        body.append(grid)
        co.append(panel)
        return co
    else:
        # seleccionar la primera y redirecionar a la vista que nos llamo
        if request.vars.keywords:
            request.vars.keywords = ''
        if request.vars.order:
            request.vars.order = ''
        parametros = request.vars
        args = request.args
        parametros.unidad_organica_id = (escuela_model.obtener_sede_central()).id
        u = URL(c=request.controller, f=request.function,
                     vars=parametros, args=args)
        redirect(u)
    return
