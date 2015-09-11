# -*- coding: utf-8 -*-
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import campus
from applications.agis.modules.db import edificio
from applications.agis.modules.db import aula


menu_lateral.append(
    Accion('Gestionar campus',
           URL('gestion_campus'), [myconf.take('roles.admin')]),
    ['gestion_campus'])

menu_lateral.append(
    Accion('Gestionar edificios',
           URL('gestion_edificio'), [myconf.take('roles.admin')]),
    ['gestion_edificio'])

menu_lateral.append(
    Accion('Gestionar aulas',
           URL('gestion_aula'), [myconf.take('roles.admin')]),
    ['gestion_aula'])

#menu_migas.append(
    #BotonConMenu(Accion('Configuración', '#', []),
        #MenuDespegable(
            #Accion('General', URL('general','index'),
                   #[myconf.take('roles.admin')]),
            #Accion('Instituto', URL('instituto','index'),
                   #[myconf.take('roles.admin')]),
            #Accion('Infraestructura', URL('infraestructura','index'),
                   #[myconf.take('roles.admin')]),
            #Accion('Seguridad', URL('appadmin','manage',args=['auth']),
                   #[myconf.take('roles.admin')]),
            #)))
menu_migas.append(Accion('Configuración', '#', []))
menu_migas.append(
    Accion('Infraestructura', URL('index'), [myconf.take('roles.admin')]))

def index():
    redirect( URL( 'gestion_campus' ) )
    return dict(message="hello from infraestructura.py")

@auth.requires_membership(myconf.take('roles.admin'))
def gestion_edificio():
    menu_migas.append(T('Gestión de edificios'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = edificio.obtener_manejo()
    return dict(manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def gestion_aula():
    menu_migas.append(T('Gestión de aulas'))
    response.view = 'infraestructura/gestion_campus.html'
    manejo = aula.obtener_manejo()
    return dict( manejo=manejo )

@auth.requires_membership(myconf.take('roles.admin'))
def gestion_campus():
    menu_migas.append(T('Gestión de campus'))
    manejo = campus.obtener_manejo()
    return dict( manejo=manejo )
