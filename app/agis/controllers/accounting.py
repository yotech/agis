# -*- coding: utf-8 -*-

response.view = "accounting/generic.html"
response.title = T('Accounting')


@auth.requires_membership('administrators')
def index():
    redirect(URL('payments'))
    return dict(message="hello from accounting.py")


@auth.requires_membership('administrators')
def payments():
    response.subtitle = T("General list")
    grid = SQLFORM.grid(db.payment,
        formargs=common_formargs,
        create=False,
    )
    return dict(grid=grid)


@auth.requires_membership('administrators')
def add_bank_payment():
    response.subtitle = T("Add bank payment")
    db.payment.person.widget = SQLFORM.widgets.autocomplete(
        request, db.person.full_name,
        id_field=db.person.id,
        min_length=1,
    )
    form = SQLFORM.factory(db.payment, db.payment_bank)
    if form.process().accepted:
        id = db.payment.insert(**db.payment._filter_fields(form.vars))
        form.vars.payment = id
        db.payment_bank.insert(**db.payment_bank._filter_fields(form.vars))
    return dict(grid=form)
