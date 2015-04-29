# -*- coding: utf-8 -*-


class School(object):
    name = ''
    academic_region = None
    classification = ''
    nature = ''
    registration_code = ''
    code = ''
    logo = ''

    def __init__(self):
        super(School, self).__init__()

    def __str__(self):
        return self.name