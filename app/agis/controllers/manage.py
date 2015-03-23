# -*- coding: utf-8 -*-

# Admin interface
@auth.requires_membership('administrators')
def index(): return dict(message=auth.user)

@auth.requires_membership('administrators')
def users():
    response.title = T('Security management')
    response.subtitle = T('User management')
    grid = SQLFORM.grid(db.auth_user,
        csv=False,
        details=False,
        fields=[db.auth_user.last_name,db.auth_user.first_name,db.auth_user.email],
        orderby=[db.auth_user.last_name],
        formargs={'showid': False}
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def rols():
    response.title = T('Security management')
    response.subtitle = T('Group management')
    grid = SQLFORM.grid(db.auth_group,
        details=False,
        csv=False,
        fields=[db.auth_group.role, db.auth_group.description],
        orderby=[db.auth_group.role],
        formargs={'showid': False}
    )
    
    return dict(grid=grid)

@auth.requires_membership('administrators')
def membership():
    response.title = T('Security management')
    response.subtitle = T('Group members')
    grid = SQLFORM.grid(db.auth_membership,
        details=False,
        csv=False,
        headers={'auth_membership.user_id': T('Name'), 'auth_membership.group_id': T('Role')},
        fields=[db.auth_membership.user_id,db.auth_membership.group_id],
        formargs={'showid': False}
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_ra():
    response.title = T('Configuration')
    response.subtitle = 'Academic Regions'
    grid = SQLFORM.grid(db.academic_region,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.academic_region.code, db.academic_region.name],
        orderby=[db.academic_region.code],
        formargs={'showid': False}
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_IHE():
    response.title = T('Configuration')
    response.subtitle = T('Institutes of Higher Education')
    grid = SQLFORM.grid(db.IHE,
        details=False,
        csv=False,
        fields=[db.IHE.code, db.IHE.name],
        searchable=False,
        maxtextlengths={'IHE.name': 100},
        formargs={'showid': False}
    )
    response.view = "manage/manage_ra.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_OU():
    grid = SQLFORM.grid(db.organic_unit,
        details=False,
        csv=False,
        fields=[db.organic_unit.code,db.organic_unit.name],
        maxtextlengths={'organic_unit.name': 100},
        formargs={'showid': False}
    )
    response.view = "manage/manage_ra.html"
    return dict(grid=grid)

@auth.requires_membership('administrators')
def manage_provinces():
    response.title = T('Configuration')
    response.subtitle = T('Provinces')
    grid=SQLFORM.grid(db.province,
        details=False,
        csv=False,
        searchable=False,
        fields=[db.province.name, db.province.ar_id],
        orderby=[db.province.name],
        formargs={'showid': False}
    )
    response.view = "manage/manage_ra.html"
    return dict(grid=grid)
