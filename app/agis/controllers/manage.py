# -*- coding: utf-8 -*-

# Admin interface
@auth.requires_membership('administrator')
def index(): return dict(message="hello from manage.py")
