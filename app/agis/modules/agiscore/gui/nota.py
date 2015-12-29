# -*- coding: utf-8 -*-
from gluon import *
from agiscore import tools
from agiscore.db import nota as nota_model
from agiscore.db import examen as examen_model
from agiscore.db import persona as persona_model
from agiscore.db import estudiante as estudiante_model
from agiscore.gui.mic import *
from agiscore.gui.mic import grid_simple

def form_editar_nota(examen, estudiante):
    co = CAT()
    db = current.db
    auth = current.auth
    T = current.T
    conf = current.conf
    rol_admin = conf.take('roles.admin')
    nota_model.definir_tabla()
    # buscar la nota
    nota = db.nota(examen_id=examen.id, estudiante_id=estudiante.id)
    db.nota.examen_id.writable = False
    db.nota.estudiante_id.writable = False
    # si no es admin entonces no se muestra el nombre
    if not auth.has_membership(role=rol_admin):
        db.nota.estudiante_id.represent = lambda v, r: \
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
    request = current.request
    rol_admin = conf.take('roles.admin')
    rol_profesor = conf.take('roles.profesor')
    nota_model.definir_tabla()
    nota_model.crear_entradas(examen.id)
    db.nota.examen_id.readable = False
    q = (db.nota.examen_id == examen.id)
    q &= (db.nota.estudiante_id == db.estudiante.id)
    q &= (db.persona.uuid == db.estudiante.uuid)
    campos = [db.persona.uuid]
    if auth.has_membership(role=rol_admin):
        campos.append(db.persona.nombre_completo)
    campos.append(db.nota.valor)
    # configurar campos
    persona_model.esconder_campos()
    estudiante_model.esconder_campos()
    db.nota.estudiante_id.readable = False
    db.persona.uuid.readable = True
    db.persona.nombre_completo.label = T('Nombre')
    db.persona.uuid.label = "UUID"
    if auth.has_membership(role=rol_admin):
        db.persona.nombre_completo.readable = True
    # enlaces en el GRID ------------------------------------------------------
    def enlaces(row):
        request = current.request
        c = request.controller
        f = request.function
        pars = request.vars
        e = db.estudiante(uuid=row.persona.uuid)
        pars['estudiante_id'] = e.id
        u = db.auth_user(auth.user.id)
        profesor = None
        asignacion = None
        if u.persona.select().first():
            profesor = u.persona.select().first().profesor.select().first()
        if profesor:
            asignacion = db.profesor_asignatura(profesor_id=profesor.id,
                        asignatura_id=examen.asignatura_id,
                        evento_id=examen.evento_id)
        nota = db.nota(examen_id=examen.id, estudiante_id=e.id)
        puede = ((auth.has_membership(role=rol_admin) or \
                 (asignacion and asignacion.es_jefe)))
        puede = puede or (auth.has_membership(role=rol_profesor) and \
                          ((nota.valor is None) and asignacion))
        from agiscore.db.evento import esta_activo
        puede = puede and esta_activo(db.evento(examen.evento_id))
        url1 = URL(c=c, f=f, args=[examen.id, 'new'],
                   vars=pars, user_signature=True)
        a1 = Accion('', url1, puede,
                    SPAN('', _class='glyphicon glyphicon-plus-sign'),
                    _class="btn btn-default",
                    _title=T("Poner nota"),)
        return CAT(a1)
    # -------------------------------------------------------------------------
    g_links = [dict(header='', body=enlaces)]
    
    text_lengths = {'persona.nombre_completo': 50,
                  'persona.uuid': 100}
    
    manejo = grid_simple(q,
                         fields=campos,
                         create=False,
                         deletable=False,
                         editable=False,
                         maxtextlengths=text_lengths,
                         links=g_links,
                         args=request.args[:1])
    
    co.append(DIV(
        DIV(H3(T("Asignación de notas para"), " ",
               examen_model.examen_format(examen),
            _class="panel-title"), _class="panel-heading"),
        DIV(manejo, _class="panel-body"),
        _class="panel panel-default"))
    return co
