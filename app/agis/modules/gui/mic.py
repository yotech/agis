# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools

__doc__ = """Miscelaneas de GUI"""

__all__ = ['Accion', 'MenuDespegable', 'BotonConMenu', 'MenuLateral',
           'MenuMigas']

class Accion(A):
    """Crea un Action que se mostrará como un enlace si el usuario actual
    tiene derechos de acceder al mismo, en caso contrario se vera desabilitado
    """
    def __init__(self, title, url, condicion, *components, **attributes):
        T = current.T

        if not condicion:
            if '_class' in attributes.keys():
                attributes['_class'] += ' text-muted disabled'
            else:
                attributes['_class'] = 'text-muted disabled'
            url = '#'
        co = CAT(T(title), *components)
        super(Accion, self).__init__(co, _href=url, **attributes)

class MenuDespegable(DIV):

    tag = 'UL'

    def __init__(self, *components, **attributes):
        if '_class' in attributes.keys():
            attributes['_class'] += ' dropdown-menu'
        else:
            attributes['_class'] = 'dropdown-menu'
        co = CAT()
        for c in components:
            co.append(LI(c))
        super(MenuDespegable, self).__init__(co, **attributes)

class MenuMigas(DIV):

    tag = 'OL'

    def xml(self):
        m = OL(_class='breadcrumb')
        for c in self.components:
                m.append(LI(c))
        ultimo = m.components[-1:][0]
        ultimo.attributes['_class'] = 'active'
        return m.xml()

class MenuLateral(DIV):

    def __init__(self, vistas, *components, **attributes):
        request = current.request
        if '_class' in attributes.keys():
            attributes['_class'] += ' list_group'
        else:
            attributes['_class'] = 'list_group'
        co = CAT()
        for c in components:
            a = 'active' if request.function in vistas else ''
            if '_class' in c.attributes.keys():
                c.attributes['_class'] += ' list-group-item {0}'.format(a)
            else:
                c.attributes['_class'] = 'list-group-item {0}'.format(a)
            c.append(SPAN(SPAN(_class='glyphicon glyphicon-hand-up'),
                          _class='badge'))
            co.append(c)
        super(MenuLateral, self).__init__(co, **attributes)

    def append(self, value, vistas):
        request = current.request
        a = 'active' if request.function in vistas else ''
        if '_class' in value.attributes.keys():
            value.attributes['_class'] += ' list-group-item {0}'.format(a)
        else:
            value.attributes['_class'] = 'list-group-item {0}'.format(a)
        value.append(' ')
        value.append(SPAN(SPAN(_class='glyphicon glyphicon-hand-up'),
                      _class='badge'))
        return super(MenuLateral, self).append(value)

class BotonConMenu(DIV):

    tag = 'DIV'

    def __init__(self, accion, menu):
        c = CAT()
        if '_class' in accion.attributes.keys():
            accion.attributes['_class'] += "btn btn-default"
        else:
            accion.attributes['_class'] = "btn btn-default"
        c.append(accion)
        c.append(A(SPAN(_class='caret'),
                   **{'_class': 'btn btn-default dropdown-toggle',
                      '_data-toggle':'dropdown',
                      '_aria-haspopup':'true',
                      '_aria-expanded':'false'}))
        c.append(menu)
        super(BotonConMenu, self).__init__(c, _class='btn-group')
