# -*- coding: utf-8 -*-
from gluon import SQLFORM, DIV, XML, CAT, SPAN, A, LI, OL, UL
from gluon import URL
from gluon import current
from gluon.storage import Storage
from agiscore import tools

__doc__ = """Miscelaneas de GUI"""

__all__ = ['Accion', 'MenuDespegable', 'BotonConMenu', 'MenuLateral',
           'MenuMigas', 'Leyenda', 'StringWidget']

# mi propia versión del helper MENU
class MYMENU(DIV):
    """
    Used to build menus

    Args:
        _class: defaults to 'web2py-menu web2py-menu-vertical'
        ul_class: defaults to 'web2py-menu-vertical'
        li_class: defaults to 'web2py-menu-expand'
        li_first: defaults to 'web2py-menu-first'
        li_last: defaults to 'web2py-menu-last'

    Use like::

        menu = MYMENU([['name', False, URL(...), [submenu]], ...])
        {{=menu}}

    """

    tag = 'ul'

    def __init__(self, data, **args):
        self.data = data
        self.attributes = args
        self.components = []
        if not '_class' in self.attributes:
            self['_class'] = 'web2py-menu web2py-menu-vertical'
        if not 'ul_class' in self.attributes:
            self['ul_class'] = 'web2py-menu-vertical'
        if not 'li_class' in self.attributes:
            self['li_class'] = 'web2py-menu-expand'
        if not 'li_first' in self.attributes:
            self['li_first'] = 'web2py-menu-first'
        if not 'li_last' in self.attributes:
            self['li_last'] = 'web2py-menu-last'
        if not 'li_active' in self.attributes:
            self['li_active'] = 'web2py-menu-active'
        if not 'mobile' in self.attributes:
            self['mobile'] = False

    def serialize(self, data, level=0):
        if level == 0:
            ul = UL(**self.attributes)
        else:
            ul = UL(_class=self['ul_class'])
        for item in data:
            if isinstance(item, LI):
                ul.append(item)
            else:
                (name, active, link) = item[:3]
                if isinstance(link, DIV):
                    li = LI(link)
                elif 'no_link_url' in self.attributes and self['no_link_url'] == link:
                    li = LI(DIV(name))
                elif isinstance(link, dict):
                    li = LI(A(name, **link))
                elif link:
                    li = LI(A(name, _href=link))
                elif not link and isinstance(name, A):
                    li = LI(name)
                else:
                    li = LI(A(name, _href='#',
                              _onclick='javascript:void(0);return false;'))
                if level == 0 and item == data[0]:
                    li['_class'] = self['li_first']
                elif level == 0 and item == data[-1]:
                    li['_class'] = self['li_last']
                if len(item) > 3 and item[3]:
                    li['_class'] = self['li_class']
                    li.append(self.serialize(item[3], level + 1))
                if active or ('active_url' in self.attributes and self['active_url'] == link):
                    if li['_class']:
                        li['_class'] = li['_class'] + ' ' + self['li_active']
                    else:
                        li['_class'] = self['li_active']
                if len(item) <= 4:
                    ul.append(li)
                else:
                    if item[4] is False:
                        li['_class'] = 'disabled'
                    ul.append(li)
        return ul

    def serialize_mobile(self, data, select=None, prefix=''):
        if not select:
            select = SELECT(**self.attributes)
        custom_items = []
        for item in data:
            # Custom item aren't serialized as mobile
            if len(item) >= 3 and (not item[0]) or (isinstance(item[0], DIV) and not (item[2])):
                # ex: ('', False, A('title', _href=URL(...), _title="title"))
                # ex: (A('title', _href=URL(...), _title="title"), False, None)
                custom_items.append(item)
            elif len(item) <= 4 or item[4] == True:
                select.append(OPTION(CAT(prefix, item[0]),
                                     _value=item[2], _selected=item[1]))
                if len(item) > 3 and len(item[3]):
                    self.serialize_mobile(
                        item[3], select, prefix=CAT(prefix, item[0], '/'))
        select['_onchange'] = 'window.location=this.value'
        # avoid to wrap the select if no custom items are present
        html = DIV(select,  self.serialize(custom_items)) if len(custom_items) else select
        return html

    def xml(self):
        if self['mobile']:
            return self.serialize_mobile(self.data, 0).xml()
        else:
            return self.serialize(self.data, 0).xml()

def grid_simple(query, **kawrgs):
    '''Construye un SQLFORM.grid con una pila de valores por defecto'''
    T = current.T
    auth = current.auth
    myconf = current.conf
    if not kawrgs.has_key('details'):
        kawrgs['details'] = False
    if not kawrgs.has_key('deletable'):
        kawrgs['deletable'] = False
    if not kawrgs.has_key('csv'):
        kawrgs['csv'] = False
    if not kawrgs.has_key('editable'):
        kawrgs['editable'] = False
    if not kawrgs.has_key('showbuttontext'):
        kawrgs['showbuttontext'] = False
    if not kawrgs.has_key('sortable'):
        kawrgs['sortable'] = False
    if not kawrgs.has_key('history'):
        history = True
    else:
        history = kawrgs['history']
        del kawrgs['history']


    puede_historial = auth.has_membership(role=myconf.take('roles.admin'))

    def _history_link(row):
        co = CAT()
        db = query._db
        tablas = db._adapter.tables(query)
        if len(tablas) > 1:
            for tbl in tablas:
                #print row.keys()
                if row.has_key(tbl):
                    if row[tbl].has_key('id'):
                        enl = URL('escuela',
                                  'historial',
                                  args=[tbl,
                                        row[tbl].id])
                        co.append(Accion(SPAN('',
                                              _class='glyphicon glyphicon-time'),
                                         enl,
                                         puede_historial,
                                         _class="btn btn-default btn-xs",
                                         _title=T("Historial {}".format(tbl))))
        else:
            enl = URL('escuela', 'historial', args=[tablas[0], row.id])
            co.append(Accion(SPAN('', _class='glyphicon glyphicon-time'),
                             enl,
                             puede_historial,
                             _class="btn btn-default btn-xs",
                             _title=T("Historial {}".format(tablas[0]))))
        return co

    # agregar enlace para historial de cambios
    if history:
        if kawrgs.has_key('links'):
            kawrgs['links'].append(dict(header='',body=_history_link))
        else:
            kawrgs['links'] = [dict(header='',body=_history_link)]

    return SQLFORM.grid(query, **kawrgs)


def StringWidget(field, value):
    w = SQLFORM.widgets.string.widget(field, value, _maxlength=field.length)
    return w

class Leyenda(DIV):

    def __init__(self, *components, **attributes):
        out_body = DIV(components, _class="panel-body")
        self.my_body = DIV(_class="btn-group", _role="group")
        out_body.append(self.my_body)
        out_body.append(XML('''
            <script>
                $(function () {
                    $('[data-toggle="popover"]').popover()
                })
            </script>'''))
        attributes['_class'] = 'panel panel-default'
        super(Leyenda, self).__init__(out_body, **attributes)

    def append(self, titulo, valores, direccion="bottom"):
        co = CAT(titulo,
                 SPAN(**{'_class': 'glyphicon glyphicon-question-sign',
                         '_aria-hidden': 'true'}))
        item = A(co,
            **{'_type': 'button',
               '_role': 'button',
               '_tabindex': '0',
               '_class': 'btn btn-default btn-xs',
               '_data-container': 'body',
               '_data-toggle': 'popover',
               '_data-placement': direccion,
               '_data-trigger': 'focus',
               '_data-content': reduce(
                    lambda x, y: x + ' ({0}){1}'.format(y[0], y[1]),
                    valores.iteritems(), '')})
        self.my_body.append(item)

class Accion(A):
    """Crea un Action que se mostrará como un enlace si el usuario actual
    tiene derechos de acceder al mismo, en caso contrario se vera desabilitado
    """
    def __init__(self, title, url, condicion, *components, **attributes):
        if not condicion:
            if '_class' in attributes.keys():
                attributes['_class'] += ' text-muted disabled'
            else:
                attributes['_class'] = 'text-muted disabled'
            url = '#'
        co = CAT(title, *components)
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
