# -*- coding: utf-8 -*-

response.view = "accounting/generic.html"
response.title = T('Accounting')


@auth.requires_membership('administrators')
def index():
    redirect(URL('payments'))
    return dict(message="hello from accounting.py")


@auth.requires_membership('administrators')
def payment_concept():
    response.subtitle = T("General list")
    grid=SQLFORM.grid(db.payment_concept,
        showbuttontext=False,
        formargs=common_formargs,
        csv=False,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def payments():
    def _payment_type(row):
        p = db(db.payment.id == row.id).select().first()
        value = 1
        if p.payment_credit.select().first():
            value = 2
        if p.payment_cash.select().first():
            value = 3
        return T(PAYMENT_TYPE[value])
    response.subtitle = T("General list")
    grid = SQLFORM.grid(db.payment,
        create=False,
        fields=[db.payment.receipt_number,
            db.payment.person,
            db.payment.payment_concept,
            db.payment.payment_date,
            db.payment.amount,
        ],
        links=[dict(header=T('Payment Type'),body=_payment_type,)],
        showbuttontext=False,
        csv=False,
    )
    return dict(grid=grid)

@auth.requires_membership('administrators')
def add_payment_credit():
    response.subtitle = T("Add credit card payment")
    db.payment_credit.payment.writable=False
    db.payment_credit.payment.readable=False
    form = SQLFORM.factory(db.payment, db.payment_credit,
        formstyle='bootstrap',
    )
    if form.process().accepted:
        id = db.payment.insert(**db.payment._filter_fields(form.vars))
        form.vars.payment = id
        db.payment_credit.insert(**db.payment_credit._filter_fields(form.vars))
        redirect(URL('payments',args=['view','payment',id],user_signature=True))
    return dict(grid=form)

@auth.requires_membership('administrators')
def add_payment_cash():
    response.subtitle = T("Add cash payment")
    db.payment_cash.payment.writable=False
    db.payment_cash.payment.readable=False
    form = SQLFORM.factory(db.payment, db.payment_cash,
        formstyle='bootstrap',
    )
    if form.process().accepted:
        id = db.payment.insert(**db.payment._filter_fields(form.vars))
        form.vars.payment = id
        db.payment_cash.insert(**db.payment_cash._filter_fields(form.vars))
        redirect(URL('payments',args=['view','payment',id],user_signature=True))
    return dict(grid=form)

@auth.requires_membership('administrators')
def add_bank_payment():
    response.subtitle = T("Add bank payment")
    db.payment_bank.payment.writable=False
    db.payment_bank.payment.readable=False
    form = SQLFORM.factory(db.payment, db.payment_bank,
        formstyle='bootstrap',
    )
    if form.process().accepted:
        id = db.payment.insert(**db.payment._filter_fields(form.vars))
        form.vars.payment = id
        db.payment_bank.insert(**db.payment_bank._filter_fields(form.vars))
        redirect(URL('payments',args=['view','payment',id],user_signature=True))
    return dict(grid=form)
