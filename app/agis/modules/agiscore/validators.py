# -*- coding: utf-8 -*-
from gluon import *


class IS_DATE_GT(IS_DATE):
    """
    Examples:
        Use as::

            >>> v = IS_DATE_GT(maximo=datetime.date(2008,1,1), \
                                     format="%m/%d/%Y",error_message="Oops")

            >>> v('03/03/2008')
            (datetime.date(2008, 3, 3), None)

            >>> v('03/03/2007')
            ('03/03/2007', 'oops')
    """
    def __init__(self,
                 maximo=None,
                 format='%Y-%m-%d',
                 error_message=None,
                 timezone=None):
        self.maximo = maximo
        if error_message is None:
            if maximo is None:
                error_message = "Enter date on or after %(max)s"
            else:
                error_message = "Enter date less than %(max)s"
        IS_DATE.__init__(self,
                         format=format,
                         error_message=error_message,
                         timezone=timezone)
        self.extremes = dict(max=self.formatter(maximo))

    def __call__(self, value):
        ovalue = value
        (value, msg) = IS_DATE.__call__(self, value)
        if msg is not None:
            return (value, msg)
        if self.maximo and self.maximo < value:
            return (ovalue, current.T(self.error_message) % self.extremes)
        return (value, None)
