# -*- coding: utf-8 -*-

response.title = T('Institute configuration')
response.view = "manage_institute/generic.html"

def index(): 
    redirect(URL('manage_IHE'))
    return dict(message="hello from manage_institute.py")


@auth.requires_membership('administrators')
def manage_IHE():
    response.subtitle = T('Institute of Higher Education')
    record = db(db.IHE.id > 0).select().first()
    form = SQLFORM(db.IHE, record,
        showid=False,
        formstyle='bootstrap',
        deletable=False
    )
    if form.process().accepted:
        response.flash = T('Updated')
    elif form.errors:
        response.flash = T('There are input errors')
    response.view = "manage_institute/manage_IHE.html"
    return dict(form=form)


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
    response.view = "manage_institute/manage_IHE.html"
    return dict(form=form)


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
        fields=[db.campus.abbr, db.campus.name, db.campus.availability],
        orderby=[db.campus.name,],
        formargs=common_formargs
    )
    response.view = "manage_institute/manage_campus.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_academic_year():
    response.subtitle = T('Academic years')
    grid=SQLFORM.grid(db.academic_year,
        fields=[db.academic_year.a_year, db.academic_year.description],
        orderby=[~db.academic_year.a_year,],
        details=False,
        searchable=False,
        csv=False,
        formargs=common_formargs,
    )
    return dict(grid=grid)
