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
        orderby=[db.municipality.code,],
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
        fields=[db.commune.name, db.commune.municipality],
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
        fields=[db.regime.name, db.regime.abbr]
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
        orderby=db.middle_school_type.name,
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
        ou = db(db.organic_unit.id > 0).select().first()
        db.middle_school.province.default = ou.province_id
        db.middle_school.province.requires = IS_IN_DB(db,'province.id',
            '%(name)s',
            zero=None,
        )
        db.middle_school.municipality.requires = IS_IN_DB(
            db(db.municipality.province == ou.province_id),
            'municipality.id',
            '%(name)s',
            zero=None,
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
def special_education():
    response.subtitle = T('Special education needs')
    grid=SQLFORM.grid(db.special_education,
        searchable=False,
        csv=False,
        details=False,
        fields=[db.special_education.code,db.special_education.name],
        orderby=db.special_education.name,
        formargs=common_formargs,
    )
    return dict(grid=grid)
