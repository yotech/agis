from agiscore.gui.mic import Accion

if not request.ajax:
    # import si se necesita
    from agiscore.gui.escuela import escuela_menu
    from agiscore.gui.unidad_organica import unidad_menu
    from agiscore.gui.inscripcion import inscripcion_menu
    # contruir el menú en orden
    evento_id = request.args(0)
    ev = db.evento(evento_id)
    ano = db.ano_academico(ev.ano_academico_id)
    unidad = db.unidad_organica(ano.unidad_organica_id)
    response.menu += escuela_menu()
    response.menu += unidad_menu(unidad.id)
    response.menu += inscripcion_menu(ev.id)
