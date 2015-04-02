# -*- coding: utf-8 -*-

common_formargs={'showid': False, 'formstyle': 'bootstrap',
    'deletable': False,
}

def index():
    return dict(message="hello from students.py")

def academic_sources():
    response.title = T('Students management')
    response.subtitle = T('Academic sources')
    grid=SQLFORM.grid(db.academic_source,
        searchable=False,
        csv=False,
        details=False,
        fields=[db.academic_source.name,db.academic_source.code],
        orderby=db.academic_source.name,
        formargs=common_formargs,
    )
    response.view = 'students/manage_as.html'
    return dict(grid=grid)

def special_education():
    response.title = T('Students management')
    response.subtitle = T('Special education needs')
    grid=SQLFORM.grid(db.special_education,
        searchable=False,
        csv=False,
        details=False,
        fields=[db.special_education.name,db.special_education.code],
        orderby=db.special_education.name,
        formargs=common_formargs,
    )
    response.view = 'students/manage_as.html'
    return dict(grid=grid)
