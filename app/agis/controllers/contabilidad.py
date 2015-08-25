# -*- coding: utf-8 -*-
from datetime import datetime
from gluon.storage import Storage
from applications.agis.modules.db import tipo_pago as tp
from applications.agis.modules.db import candidatura
from applications.agis.modules.db import pago
from applications.agis.modules.db import evento
from applications.agis.modules.db import examen
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import ano_academico
from applications.agis.modules.db import persona
from applications.agis.modules.db import estudiante
from applications.agis.modules.db import examen_aula_estudiante

sidenav.append(
    [T('Tipos de Pagos'), # Titulo del elemento
     URL('tipo_pago'), # url para el enlace
     ['tipo_pago'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Registrar pago de inscripción'), # Titulo del elemento
     URL('registrar_pago_inscripcion'), # url para el enlace
     ['registrar_pago_inscripcion'],] # en funciones estará activo este item
)

migas.append(
    tools.split_drop_down(
        Storage(dict(url='#', texto=T('Contabilidad'))),
        [Storage(dict(url=URL('tipo_pago'),
                      texto=T('Tipos de Pagos'))),
         Storage(dict(url=URL('registrar_pago_inscripcion'),
                      texto=T('Registrar pago de inscripción'))),
         ]
        )
    )

def index():
    redirect(URL('tipo_pago'))
    return dict(sidenav=sidenav,message="hello from contabilidad.py")

@auth.requires_membership('administrators')
def registrar_pago_inscripcion():
    unidad_organica.definir_tabla()
    ano_academico.definir_tabla()
    evento.definir_tabla()
    persona.definir_tabla()
    estudiante.definir_tabla()

    # buscar un tipo de pago que coincida en nombre con el tipo de evento
    tipo_pago = db(db.tipo_pago.nombre == evento.evento_tipo_represent('1',None)).select().first()
    if not tipo_pago:
        session.flash=T("Defina un tipo de pago para {0}".format(evento.evento_tipo_represent('1',None)))
        redirect( URL( 'tipo_pago') )

    context = dict( sidenav=sidenav )
    context['mensaje'] = ''
    if not request.vars.unidad_organica_id:
        # -- seleccionar unidad organica
        migas.append(T('Registrar pago de inscripción'))
        if db(unidad_organica.conjunto()).count() > 1:
            # Si hay más de una UO
            context['manejo'] = tools.selector(unidad_organica.conjunto(),
                                                 [db.unidad_organica.codigo,
                                                  db.unidad_organica.nombre],
                                                 'unidad_organica_id',
                                                 )
            context['mensaje'] = "Seleccione la unidad orgánica"
            return context
        else:
            # seleccionar la primera y pasar directamente al paso 2
            unidad_organica_id = (escuela.obtener_sede_central()).id
            redirect(URL('registrar_pago_inscripcion',vars={'unidad_organica_id': unidad_organica_id}))
    else:
        migas.append(A(T('Registrar pago de inscripción'),
                       _href=URL('registrar_pago_inscripcion')))
        unidad_organica_id = int(request.vars.unidad_organica_id)
        context['unidad_organica'] = db.unidad_organica(unidad_organica_id)
    # mostrar selector de eventos
    if not request.vars.evento_id:
        migas.append(context['unidad_organica'].nombre)
        tmp = db(db.ano_academico.unidad_organica_id == unidad_organica_id).select(db.ano_academico.id)
        annos = [i['id'] for i in tmp]
        if not annos:
            session.flash = T('No se han definido Años académicos para ') +  context['unidad_organica'].nombre
            redirect(URL('registrar_pago_inscripcion'))
        conjunto = evento.conjunto(db.evento.ano_academico_id.belongs(annos) &
                                   (db.evento.tipo == '1') &
                                   (db.evento.estado == True))
        context['manejo'] = tools.selector(conjunto,
                                             [db.evento.nombre,
                                              db.evento.ano_academico_id],
                                             'evento_id',
                                             vars=dict(unidad_organica_id=unidad_organica_id))
        context['mensaje'] = "Seleccione el evento inscripción"
        return context
    else:
        evento_id = int(request.vars.evento_id)
        context['evento'] = db.evento(evento_id)
        migas.append(A(context['unidad_organica'].nombre,
                       _href=URL('registrar_pago_inscripcion',
                                vars={'unidad_organica_id': unidad_organica_id})))

    if not request.vars.persona_id:
        # Mostrar un selector para las candidaturas que pueden hacer pago de inscripción en la UO y evento
        # seleccionados
        migas.append(context['evento'].nombre)
        query = ((db.persona.id == db.estudiante.persona_id) &
                 (db.candidatura.estudiante_id == db.estudiante.id) &
                 (db.candidatura.unidad_organica_id == unidad_organica_id) &
                 (db.candidatura.ano_academico_id == context['evento'].ano_academico_id) &
                 (db.candidatura.estado_candidatura == '1'))
        campos=[db.persona.id, db.persona.nombre_completo]
        db.persona.nombre_completo.label = T('Nombre')
        db.persona.id.readable = False
        context['manejo'] = tools.selector(query,
            campos,
            'persona_id',
            vars=dict(unidad_organica_id=unidad_organica_id,
                      evento_id=evento_id)
        )
        context['mensaje'] = "Seleccione persona a realizar el pago"
        return context
    else:
        persona_id = int(request.vars.persona_id)
        context['persona'] = db.persona(persona_id)
        migas.append(A(context['evento'].nombre,
                       _href=URL('registrar_pago_inscripcion',
                            vars=dict(unidad_organica_id=unidad_organica_id,
                                      evento_id=evento_id))))

    db.pago.tipo_pago_id.default=tipo_pago.id
    db.pago.tipo_pago_id.writable=False
    db.pago.cantidad.default=tipo_pago.cantidad
    db.pago.cantidad.writable=False
    db.pago.persona_id.default = persona_id
    db.pago.persona_id.writable = False
    manejo = SQLFORM(db.pago, submit_button=T( 'Guardar' ))
    if manejo.process().accepted:
        candidatura.inscribir(persona_id, evento_id)
        # -- agregado por #70: generar los examenes de inscripción para el candidato
        cand = candidatura.obtener_candidatura_por_persona(persona_id)
        examenes_ids = examen.generar_examenes_acceso(cand)
        # -- redistribuir las aulas para el examen
        # -- TODO: quitar si se pone lento
#         for id in examenes_ids:
#             examen_aula_estudiante.distribuir_estudiantes(id)
        # -----------------------------------------------------------
        session.flash=T( 'Pago registrado' )
        redirect(URL('registrar_pago_inscripcion', vars=dict(unidad_organica_id=unidad_organica_id,
                                                             evento_id=evento_id)))
    context['manejo'] = manejo
    return context

@auth.requires_membership('administrators')
def tipo_pago():
    migas.append(T('Tipos de pagos'))
    manejo = tp.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )
