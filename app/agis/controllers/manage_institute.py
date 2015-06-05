# -*- coding: utf-8 -*-
from applications.agis.modules.db import escuela

response.title = T('Institute configuration')
response.view = "manage_institute/generic.html"

def index(): 
    redirect(URL('configurar_escuela'))
    return dict(message="hello from manage_institute.py")


@auth.requires_membership('administrators')
def configurar_escuela():
    response.subtitle = T('Escuela')
    record = escuela.obtener_escuela()
    form_escuela = SQLFORM(db.escuela, record,
        showid=False,
        formstyle='bootstrap',
        deletable=False
    )
    if form_escuela.process().accepted:
        response.flash = T('Cambios guardados')
    elif form_escuela.errors:
        response.flash = T('Existen errores en los datos de la escuela')
    response.view = "manage_institute/manage_IHE.html"
    return dict(form_escuela=form_escuela)


@auth.requires_membership('administrators')
def manage_OU():
    response.subtitle = T('Organic unit')
    record = db(db.organic_unit.id > 0).select().first()
    form = SQLFORM(db.organic_unit, record,
        showid=False,
        formstyle='bootstrap',
        deletable=False
    )
    if form.process().accepted:
        response.flash = T('Updated')
    elif form.errors:
        response.flash = T('There are input errors')
#     response.view = "manage_institute/manage_IHE.html"
    return dict(grid=form)


@auth.requires_membership('administrators')
def manage_career():
    response.subtitle = T('Careers')
    if request.args(0) == 'new':
        careers = db(db.career.career_des_id == None).select(
            db.career_des.ALL,db.career.ALL,
            orderby=db.career_des.name,
            left=db.career.on(db.career_des.id==db.career.career_des_id),
        )
        if not careers:
            session.flash = T('No more careers for add')
            redirect(URL('manage_career'))
        values = dict()
        for r in careers:
            values[r.career_des.id] = r.career_des.name
        db.career.career_des_id.requires = IS_IN_SET(values,zero=None)
    grid=SQLFORM.grid(db.career,
        fields=[db.career.career_des_id, db.career.organic_unit_id],
        maxtextlengths={
            'career.career_des_id': 100,
            'career.organic_unit_id': 100,
        },
        showbuttontext=False,
        editable=False,
        details=False,
        formargs=common_formargs,
        csv=False,
        orderby=[db.career.career_des_id],
    )
    return dict(grid=grid)


@auth.requires_membership('administrators')
def manage_ou_regime():
    response.subtitle = T('Organic unit regimes')
    if request.args(0) == 'new':
        regimes = db(db.ou_regime.organic_unit_id == None).select(
            db.regime.ALL, db.ou_regime.ALL, 
            left=db.ou_regime.on(db.regime.id==db.ou_regime.regime_id)
        )
        if not regimes:
            session.flash = T('No regimes descriptions left')
            redirect(URL('manage_ou_regime'))
        values = dict()
        for r in regimes:
            values[r.regime.id] = r.regime.name
        db.ou_regime.regime_id.requires = IS_IN_SET(values,
            zero=None,
            error_message=T('Choose one regime')
        )
    grid = SQLFORM.grid(db.ou_regime,
        csv=False,
        showbuttontext=False,
        searchable=False,
        details=False,
        fields=[db.ou_regime.regime_id, db.ou_regime.organic_unit_id],
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def campus_create_ajax():
    form = SQLFORM(db.campus,
        formstyle="divs",
    )
    if form.process().accepted:
        redirect(request.env.http_web2py_component_location,client_side=True)
    response.view = "manage_institute/campus_create_ajax.load"
    return dict(form=form)

@auth.requires_membership('administrators')
def campus_list_ajax():
    grid = SQLFORM.grid(db.campus)
    response.view = "manage_institute/campus_list_ajax.load"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_campus():
    response.subtitle = T("Campus")
    grid = SQLFORM.grid(db.campus,
        details=False,
        csv=False,
        showbuttontext=False,
        fields=[db.campus.abbr, db.campus.name, db.campus.availability],
        orderby=[db.campus.name,],
        formargs=common_formargs
    )
    response.view = "manage_institute/manage_campus.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_building():
    response.subtitle = T("Buildings")
    grid = SQLFORM.grid(db.building,
        details=False,
        showbuttontext=False,
        csv=False,
        fields=[db.building.abbr, db.building.name,
            db.building.availability,
            db.building.campus
        ],
        orderby=[db.building.name,],
        formargs=common_formargs
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_classroom():
    response.subtitle = T("Classrooms")
    grid = SQLFORM.grid(db.classroom,
        details=False,
        showbuttontext=False,
        csv=False,
        fields=[db.classroom.name,
            db.classroom.c_size,
            db.classroom.availability,
            db.classroom.building,
        ],
        orderby=[db.classroom.name,],
        formargs=common_formargs
    )
    return dict(grid=grid)

#@auth.requires_membership('administrators')
#def manage_building_ajax():
    #campus_id = int(request.args(0))
    #query = db((db.building.id > 0) & (db.building.campus == campus_id))
    #db.building.campus.default = campus_id
    #db.building.campus.readable = False
    #db.building.campus.writable = False
    #grid = SQLFORM.grid(query,
        #details=False,
        #csv=False,
        #searchable=False,
        #args=[int(request.args(0))],
        ##fields=[db.building.abbr, db.building.name, db.building.availability],
        ##orderby=[db.building.name,],
        #formargs=common_formargs
    #)
    #return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_academic_year():
    response.subtitle = T('Academic years')
    grid=SQLFORM.grid(db.academic_year,
        fields=[db.academic_year.a_year, db.academic_year.description],
        orderby=[~db.academic_year.a_year,],
        details=False,
        showbuttontext=False,
        searchable=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_course():
    response.subtitle = T('Courses')
    grid=SQLFORM.grid(db.course,
        details=False,
        showbuttontext=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_student_group():
    response.subtitle = T('Student groups')
    db.student_group.id.readable = False
    db.student_group.id.writable = False
    grid=SQLFORM.grid(db.student_group,
        details=False,
        showbuttontext=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_gsa_spaces():
    response.subtitle = T('Granted access spaces')
    db.gsa_spaces.id.readable=False
    db.gsa_spaces.id.writable=False
    grid=SQLFORM.grid(db.gsa_spaces,
        details=False,
        showbuttontext=False,
        csv=False,
        formargs=common_formargs,
        maxtextlengths={'gsa_spaces.career': 100,},
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def academic_level():
    response.subtitle = T('Academic levels')
    db.academic_level.id.readable = False
    db.academic_level.id.writable = False
    grid=SQLFORM.grid(db.academic_level,
        details=False,
        showbuttontext=False,
        searchable=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)


@auth.requires_membership('administrators')
def academic_plan():
    response.subtitle = T('Academic Plans')
    db.academic_plan.id.readable = False
    db.academic_plan.id.writable = False
    grid=SQLFORM.grid(db.academic_plan,
        details=False,
        showbuttontext=False,
        searchable=False,
        csv=False,
        formargs=common_formargs,
        maxtextlengths={'academic_plan.career_id': 100,},
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_department():
    response.subtitle = T("Department")
    grid = SQLFORM.grid(db.department,
        details=False,
        showbuttontext=False,
        csv=False,
        fields=[db.department.name,
            db.department.organic_unit,
        ],
        orderby=[db.department.name,],
        formargs=common_formargs
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_ou_event():
    response.subtitle = T("Events")
    grid = SQLFORM.grid(db.ou_event,
        details=False,
        showbuttontext=False,
        csv=False,
        fields=[db.ou_event.name,
            db.ou_event.ou_event_type,
            db.ou_event.academic_year,
            db.ou_event.start_date,
            db.ou_event.end_date,
            db.ou_event.availability,
        ],
        orderby=[db.ou_event.academic_year, db.ou_event.name],
        formargs=common_formargs
    )
    return dict(grid=grid)
