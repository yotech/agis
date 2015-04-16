# -*- coding: utf-8 -*-

response.view = "candidates/generic.html"
response.title = T('Candidates management')

@auth.requires_membership('administrators')
def index():
    redirect(URL('with_debts'))
    return dict(message="hello from candidates.py")

@auth.requires_membership('administrators')
def create():
    cond=(db.candidate_debt.is_worker == True)
    db.candidate_debt.work_name.show_if = cond
    db.candidate_debt.profession_name.show_if = cond
    db.candidate_debt.person.widget = SQLFORM.widgets.autocomplete(
        request, db.person.full_name,
        id_field=db.person.id,
        min_length=1,
    )
    if request.vars.is_worker:
        contrain = [IS_NOT_EMPTY()]
        db.candidate_debt.work_name.requires=contrain
        db.candidate_debt.profession_name.requires=contrain
    form = SQLFORM(db.candidate_debt,
        formstyle='divs'
    )
    if form.process(hideerror=True).accepted:
        redirect(URL('candidates','index'))

    response.view = "candidates/create.html"
    response.subtitle = T("Add candidate")
    return dict(form=form)

def __with_debts_link_person(row):
    person_data = A(T('Edit personal data'),
        _class='btn',
        _href=URL('manage_general','manage_persons',
            args=['edit','person',row.person.id],
            user_signature=True
        ),
    )

    return CAT(person_data)

def edit_candidate_careers():
    candidate = db.candidate_debt[int(request.args(0))]
    db.candidate_career.candidate.default = candidate.id
    db.candidate_career.candidate.readable = False
    db.candidate_career.candidate.writable = False
    ou = db.organic_unit[candidate.organic_unit]
    values = dict()
    for career in ou.career.select():
        career_des = db.career_des[career.career_des_id]
        values[career.id] = career_des.name
    db.candidate_career.career.requires = IS_IN_SET(values, zero=None)
    grid = SQLFORM.grid(db.candidate_career,args=[candidate.id],
        details=False,
        searchable=False,
        csv=False,
        fields=[db.candidate_career.priority,db.candidate_career.career],
        maxtextlengths={'candidate_career.career': 100},
        orderby=[db.candidate_career.priority],
        formargs=common_formargs,
    )
    response.view = 'candidates/edit_candidate_careers.load'
    return dict(grid=grid)

@auth.requires_membership('administrators')
def with_debts():
    if request.args(0) == 'edit':
        cond=(db.candidate_debt.is_worker == True)
        db.candidate_debt.work_name.show_if = cond
        db.candidate_debt.profession_name.show_if = cond
        db.candidate_debt.person.writable = False
        db.candidate_debt.person.readable = False
        if request.vars.is_worker:
            contrain = [IS_NOT_EMPTY()]
            db.candidate_debt.work_name.requires=contrain
            db.candidate_debt.profession_name.requires=contrain
        response.view = "candidates/edit.html"
    db.person.id.readable = False
    db.candidate_debt.id.readable = False
    grid=SQLFORM.grid(
        db.candidate_debt,
        left=db.person.on((db.person.id == db.candidate_debt.person)&(db.person.sys_status == True)),
        create=False,
        details=False,
        editable=True,
        deletable=False,
        exportclasses=dict(csv_with_hidden_cols=False,
            xml=False,
            tsv=False,
            html=False,
            tsv_with_hidden_cols=False,
            json=False,
        ),
        fields=[db.person.id,db.person.full_name,db.candidate_debt.id],
        formargs=common_formargs,
        links=[dict(header='',body=__with_debts_link_person)]
    )
    return dict(grid=grid)
