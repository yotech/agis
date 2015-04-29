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
        create=False,
        fields=[db.payment.id,
            db.payment.person,
            db.payment.payment_type,
            db.payment.payment_date,
            db.payment.amount
        ],
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
    db.payment_bank.payment.writable=False
    db.payment_bank.payment.readable=False
    form = SQLFORM.factory(db.payment, db.payment_bank,
        formstyle='bootstrap'
    )
    if form.process().accepted:
        id = db.payment.insert(**db.payment._filter_fields(form.vars))
        form.vars.payment = id
        db.payment_bank.insert(**db.payment_bank._filter_fields(form.vars))
        redirect(URL('payments',args=['view','payment',id],user_signature=True))
    return dict(grid=form)
