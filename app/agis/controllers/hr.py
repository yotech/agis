# -*- coding: utf-8 -*-
# try something like
response.view = "hr/generic.html"

def index(): return dict(message="hello from hr.py")

@auth.requires_membership('administrators')
def teachers_management():
    return dict(grid=None)

def _teacher_person_id_represent(value, row):
        person = db.person[int(value)]
        return CAT(person.full_name, ' ',
            A(
                SPAN('',
                    _class="icon-pencil"
                ),
                _class="btn btn-default",
                _href=URL('manage_general', 'manage_persons',
                    args=['edit','person',value],
                    user_signature=True,
                ),
                _title=T("Edit personal info")
            )
        )

@auth.requires_membership('administrators')
def teacher_list():
    db.teacher.id.readable=False
    db.teacher.id.writable=False
    db.teacher.person_id.writable = False
    db.teacher.person_id.represent = _teacher_person_id_represent
    grid = SQLFORM.grid(db.teacher,
        create=False,
        details=False,
        showbuttontext=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def teacher_assign_course():
    db.teacher_course.id.readable=False
    db.teacher_course.id.writable=False
    grid=SQLFORM.grid(db.teacher_course,
        details=False,
        csv=False,
        showbuttontext=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
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
    db.teacher.person_id.writable = False
    db.teacher.person_id.readable = False
    form = SQLFORM.factory(db.person,db.teacher,formstyle='divs')
    if form.process().accepted:
        id = db.person.insert(**db.person._filter_fields(form.vars))
        form.vars.person_id = id
        db.teacher.insert(**db.teacher._filter_fields(form.vars))
        session.flash=T("Teacher added")
        redirect(URL('teacher_add'))
    return dict(form=form)
