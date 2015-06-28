# -*- coding: utf-8 -*-

def index():
    raise HTTP(403)
    return dict(message="hello from tools.py")

def obtener_comunas():
    if request.ajax:
        municipio_id = int( request.vars.dir_municipio_id )
        resultado = ''
        for c in comuna.obtener_comunas( municipio_id ):
            op = OPTION(c.nombre, _value=c.id)
            resultado += op.xml()
    else:
        raise HTTP(404)
    return resultado

def obtener_municipios():
    if request.ajax:
        provincia_id = int( request.vars.dir_provincia_id )
        resultado = ''
        for m in municipio.obtener_municipios( provincia_id ):
            op = OPTION( m.nombre,_value=m.id )
            resultado += op.xml()
    else:
        raise HTTP(404)
    return resultado
