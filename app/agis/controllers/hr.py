# -*- coding: utf-8 -*-
# try something like
response.view = "hr/generic.html"

def index(): return dict(message="hello from hr.py")

def teachers_management():
    return dict(grid=None)

def teacher_list():
    return dict(grid=None)

def teacher_add():
    response.view = "hr/teacher_add.html"
    response.subtitle = T("Add teacher")
    db.person.email.requires = IS_EMAIL() if request.vars.email else None
    if request.vars.municipality:
        municipality = db.municipality[int(request.vars.municipality)]
    else:
        municipality = db(db.municipality.id > 0).select().first()
        if not municipality:
            session.flash = T('Add some municipalities first')
            redirect(URL('manage_general','index'))
        db.person.municipality.default = municipality.id
    db.person.commune.requires = IS_IN_DB(
        db(db.commune.municipality == municipality.id),
        'commune.id',
        '%(name)s',
        zero=None,
        error_message=T('Commune is required'),
    )
    db.person.place_of_birth.widget = SQLFORM.widgets.autocomplete(
        request, db.commune.name,
        id_field=db.commune.id,
        min_length=1,
        orderby=db.commune.name,
    )
    form = SQLFORM.factory(db.person,db.teacher,formstyle='divs')
    return dict(form=form)
