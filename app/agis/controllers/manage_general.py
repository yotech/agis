# -*- coding: utf-8 -*-

response.view = "manage_general/generic.html"
response.title = T('General configuration')

def index(): 
    redirect(URL('manage_ra'))
    return dict(message="hello from manage_general.py")


@auth.requires_membership('administrators')
def manage_ra():
    response.subtitle = T('Academic Regions')
    grid = SQLFORM.grid(db.academic_region,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.academic_region.code, db.academic_region.name],
        orderby=[db.academic_region.code],
        formargs=common_formargs,
    )
    return dict(grid=grid)


@auth.requires_membership('administrators')
def manage_career_des():
    response.subtitle = T('Careers Descriptions')
    grid = SQLFORM.grid(db.career_des,
        details=False,
        fields=[db.career_des.code, db.career_des.name],
        orderby=[db.career_des.name],
        maxtextlengths={'career_des.name': 100},
        exportclasses=dict(csv_with_hidden_cols=False,
            xml=False,
            tsv=False,
            html=False,
            tsv_with_hidden_cols=False,
            json=False,
        ),
        formargs=common_formargs,
    )
    
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_provinces():
    response.subtitle = T('Provinces')
    grid=SQLFORM.grid(db.province,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.province.code,db.province.name, db.province.ar_id],
        orderby=[db.province.name],
        formargs=common_formargs,
    )
    
    return dict(grid=grid)


@auth.requires_membership('administrators')
def manage_municipality():
    response.subtitle = T('Municipalities')
    grid = SQLFORM.grid(db.municipality,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.municipality.code, db.municipality.name,
            db.municipality.province,
        ],
        orderby=[db.municipality.province, db.municipality.code],
        formargs=common_formargs,
    )
    
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_commune():
    municipalities = db(db.municipality.id > 0).select()
    if not municipalities:
        session.flash=T('Define some municipalities first')
        redirect(URL('manage_municipality'))
    response.subtitle = T('Communes')
    grid = SQLFORM.grid(db.commune,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.commune.code, db.commune.name, db.commune.municipality],
        orderby=[db.commune.municipality, db.commune.code],
        formargs=common_formargs,
    )

    return dict(grid=grid)


@auth.requires_membership('administrators')
def manage_regime():
    response.subtitle = T('Regimes')
    grid = SQLFORM.grid(db.regime,
        searchable=False,
        csv=False,
        details=False,
        formargs=common_formargs,
        fields=[db.regime.code, db.regime.name, db.regime.abbr]
    )
    
    return dict(grid=grid)


@auth.requires_membership('administrators')
def manage_idt():
    response.subtitle = T('Identity card types')
    grid = SQLFORM.grid(db.identity_card_type,
        searchable=False,
        csv=False,
        details=False,
        formargs=common_formargs,
        fields=[db.identity_card_type.name],
        maxtextlengths={'identity_card_type.name': 100},
    )
    
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_middle_school_types():
    response.subtitle = T('Middle school types')
    grid = SQLFORM.grid(db.middle_school_type,
        searchable=False,
        csv=False,
        details=False,
        formargs=common_formargs,
        fields=[db.middle_school_type.code,db.middle_school_type.name],
        orderby=db.middle_school_type.code,
        maxtextlengths={'middle_school_type.name': 100},
    )

    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_middle_school():
    mst = db(db.middle_school_type.id > 0).select()
    if not mst:
        session.flash=T('Define some school types first')
        redirect(URL('manage_middle_school_types'))
    response.subtitle = T('Middle schools')
    if request.args(0) == 'new':
        if request.post_vars.province:
            province = db.province[int(request.post_vars.province)]
        else:
            ou = db(db.organic_unit.id > 0).select().first()
            province = db.province[ou.province_id]
            db.middle_school.province.default = ou.province_id
        db.middle_school.province.requires = IS_IN_DB(db,'province.id',
            '%(name)s',
            zero=None,
        )
        db.middle_school.municipality.requires = IS_IN_DB(
            db(db.municipality.province == province.id),
            'municipality.id',
            '%(name)s',
            zero=None,
            error_message = T("Municipality is required"),
        )
    grid = SQLFORM.grid(db.middle_school,
        csv=False,
        details=False,
        formargs=common_formargs,
        fields=[db.middle_school.code,db.middle_school.name],
        orderby=db.middle_school.name,
        maxtextlengths={'middle_school.name': 100},
    )
    response.view = "manage_general/manage_middle_school.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def get_municipality():
    province_id = request.vars.province
    municipalities = db(db.municipality.province == province_id).select()
    rs = ''
    for muni in municipalities:
        op = OPTION(muni.name, _value=muni.id)
        rs += op.xml()
    return rs

@auth.requires_membership('administrators')
def get_communes():
    """ from a municipality id get his communes as a options list"""
    municipality_id = request.vars.municipality
    communes = db(db.commune.municipality == municipality_id).select()
    rs = ''
    for commune in communes:
        op = OPTION(commune.name, _value=commune.id)
        rs += op.xml()
    return rs

@auth.requires_membership('administrators')
def manage_persons():
    if request.vars.email:
        db.person.email.requires = IS_EMAIL(
            error_message=T('Invalid email')
        )
    else:
        db.person.email.requires = None
    if request.args(0) == 'new':
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
    if request.args(0) == 'edit':
        id = int(request.args(2))
        person = db.person[id]
        if request.vars.municipality:
            municipality = db.municipality[int(request.vars.municipality)]
        else:
            municipality = db.municipality[person.municipality]
        db.person.commune.requires = IS_IN_DB(
            db(db.commune.municipality == municipality.id),
            'commune.id',
            '%(name)s',
            zero=None,
            error_message=T('Commune is required'),
        )
    grid=SQLFORM.grid(db.person,
        formargs={'showid': False, 'formstyle': 'divs',
            'deletable': False,
        },
        details=False,
        exportclasses=dict(csv_with_hidden_cols=False,
            xml=False,
            tsv=False,
            html=False,
            tsv_with_hidden_cols=False,
            json=False,
        ),
        maxtextlengths={'person.full_name': 100},
        editable=True,
        create=True,
        fields=[db.person.full_name,db.person.email],
        orderby=[db.person.full_name],
    )
    response.view = "manage_general/manage_persons.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def create_person():
    form = SQLFORM(db.person,
        formstyle="bootstrap",
    )
    next = request.vars.next if request.vars.next else URL('manage_persons')
    if form.process(next=next).accepted:
        redirect(URL('manage_persons'))
    response.view = "manage_general/create_person.html"
    return dict(form=form)

@auth.requires_membership('administrators')
def special_education():
    response.subtitle = T('Special education needs')
    grid=SQLFORM.grid(db.special_education,
        searchable=False,
        csv=False,
        details=False,
        fields=[db.special_education.code,db.special_education.name],
        orderby=db.special_education.code,
        formargs=common_formargs,
    )
    return dict(grid=grid)
