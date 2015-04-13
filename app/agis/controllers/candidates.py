# -*- coding: utf-8 -*-

response.view = "candidates/generic.html"
response.title = T('Candidates management')

def index(): return dict(message="hello from candidates.py")

def create():
    cond=(db.candidate_debt.is_worker == True)
    db.candidate_debt.work_name.show_if = cond
    db.candidate_debt.profession_name.show_if = cond
    form = SQLFORM(db.candidate_debt,
        formstyle='bootstrap'
    )
    if form.process().accepted:
        redirect(URL('candidates','index'))
    return dict(form=form)

def with_debts():
    query = (db.candidate_debt.person == db.person.id)
    grid=SQLFORM.grid(
        query,
        create=False,
        details=False,
        fields=[db.person.full_name,
            db.person.phone_number,
            db.person.email,
        ]
    )
    return dict(grid=grid)
