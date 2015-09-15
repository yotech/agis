# -*- coding: utf-8 -*-
from gluon import *
from applications.agis.modules import tools
from applications.agis.modules.db import nota as nota_model
from applications.agis.modules.db import examen as examen_model
from applications.agis.modules.db import persona as persona_model
from applications.agis.modules.db import estudiante as estudiante_model
from applications.agis.modules.gui.mic import *

def form_editar_nota(examen, estudiante):
    co = CAT()
    db = current.db
    T = current.T
    conf = current.conf
    rol_admin = conf.take('roles.admin')
    rol_profesor = conf.take('roles.profesor')
    rol_jasig = conf.take('roles.jasignatura')
    nota_model.definir_tabla()
    # buscar la nota
    nota = db.nota(examen_id=examen.id,estudiante_id=estudiante.id)
    db.nota.examen_id.writable = False
    db.nota.estudiante_id.writable = False
    # si no es admin ni j de asignatura entonces no se muestra el nombre
    if not tools.tiene_rol([rol_admin, rol_jasig]):
        db.nota.estudiante_id.represent = lambda v,r: \
            db.estudiante(r.estudiante_id).uuid
        db.nota.estudiante_id.label = "UUID"
    manejo = SQLFORM(db.nota, record=nota)
    co.append(DIV(
        DIV(H3(T("Asignación de nota para"), " ",
               examen_model.examen_format(examen),
            _class="panel-title"), _class="panel-heading"),
        DIV(manejo, _class="panel-body"),
        _class="panel panel-default"))
    return (co, manejo)

def grid_asignar_nota(examen):
    """Retorna un grid para manejo de las notas de un examen"""
    co = CAT()
    if not examen:
        return co
    auth = current.auth
    if not auth.user:
        return co
    db = current.db
    T = current.T
    conf = current.conf
    rol_admin = conf.take('roles.admin')
    rol_profesor = conf.take('roles.profesor')
    rol_jasig = conf.take('roles.jasignatura')
    nota_model.definir_tabla()
    nota_model.crear_entradas(examen.id)
    db.nota.examen_id.readable = False
    q = (db.nota.examen_id == examen.id)
    q &= (db.nota.estudiante_id == db.estudiante.id)
    q &= (db.persona.uuid == db.estudiante.uuid)
    campos = [db.persona.uuid]
    if tools.tiene_rol([rol_admin, rol_jasig]):
        campos.append(db.persona.nombre_completo)
    campos.append(db.nota.valor)
    # configurar campos
    persona_model.esconder_campos()
    estudiante_model.esconder_campos()
    db.nota.estudiante_id.readable = False
    db.persona.uuid.readable = True
    db.persona.nombre_completo.label = T('Nombre')
    db.persona.uuid.label = "UUID"
    if tools.tiene_rol([rol_admin, rol_jasig]):
        db.persona.nombre_completo.readable = True
    # enlaces en el GRID ------------------------------------------------------
    def enlaces(row):
        request = current.request
        c = request.controller
        f = request.function
        pars = request.vars
        e = db.estudiante(uuid=row.persona.uuid)
        if not 'examen_id' in pars.keys():
            pars['examen_id'] = examen.id
        if not 'estudiante_id' in pars.keys():
            pars['estudiante_id'] = e.id
        roles_full = tools.tiene_rol([rol_admin, rol_jasig])
        url1 = '#'
        a = CAT()
        if roles_full:
            url1 = URL(c=c, f=f, args=['new'], vars=pars, user_signature=True)
            a1 = Accion('', url1, [rol_admin, rol_jasig, rol_profesor],
                        SPAN('', _class='glyphicon glyphicon-plus-sign'),
                        _class="btn btn-default",
                        _title=T("Poner nota"),)
        elif tools.tiene_rol([rol_profesor]):
            # si es olo un profesor verificar que no haya editado esta nota
            # anteriormente.
            nota = db.nota(examen_id=examen.id,estudiante_id=e.id)
            if nota.valor != None:
                # ya se ha puesto la nota, no poner el boton
                url1 = URL(c=c, f=f, args=['new'], vars=pars,
                    user_signature=True)
                a1 = Accion('', url1, ['no_roles_no_action'],
                            SPAN('', _class='glyphicon glyphicon-plus-sign'),
                            _class="btn btn-default",
                            _title=T("Poner nota"),)
            else:
                url1 = URL(c=c, f=f, args=['new'], vars=pars,
                    user_signature=True)
                a1 = Accion('', url1, [rol_profesor],
                            SPAN('', _class='glyphicon glyphicon-plus-sign'),
                            _class="btn btn-default",
                            _title=T("Poner nota"),)
        return CAT(a1)
    # -------------------------------------------------------------------------
    g_links = [dict(header='', body=enlaces)]
    manejo = tools.manejo_simple(q, campos=campos,
        crear=False, buscar=True, borrar=False, editable=False,
        enlaces=g_links)
    co.append(DIV(
        DIV(H3(T("Asignación de notas para"), " ",
               examen_model.examen_format(examen),
            _class="panel-title"), _class="panel-heading"),
        DIV(manejo, _class="panel-body"),
        _class="panel panel-default"))
    return co
