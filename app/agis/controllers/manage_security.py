# -*- coding: utf-8 -*-
response.view = 'manage_security/generic.html'

def index():
    redirect(URL('manage_security','users'))
    return dict(message="hello from manage_security.py")

@auth.requires_membership('administrators')
def users():
    response.title = T('Security management')
    response.subtitle = T('User management')
    grid = SQLFORM.grid(db.auth_user,
        csv=False,
        details=False,
        fields=[db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email],
        orderby=[db.auth_user.first_name],
        formargs=common_formargs,
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
        formargs=common_formargs,
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
        formargs=common_formargs,
    )
    return dict(grid=grid)
