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

@auth.requires_membership('administrators')
def with_debts():
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
        fields=[db.person.full_name,
            db.person.phone_number,
            db.person.email,
        ],
        formargs=common_formargs,
    )
    return dict(grid=grid)
