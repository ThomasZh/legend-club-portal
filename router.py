# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.auth import auth_email
from foo.portal import portal_quicktravel


def map():

    config = [

        # homepage
        (r'/', getattr(portal_quicktravel, 'QuickTravelIndexHandler')),

        (r'/club/auth/login', getattr(auth_email, 'AuthEmailLoginHandler')),
        (r'/club/auth/register', getattr(auth_email, 'AuthEmailRegisterHandler')),
        (r'/club/auth/forgot-pwd', getattr(auth_email, 'AuthEmailForgotPwdHandler')),
        (r'/club/auth/reset-pwd', getattr(auth_email, 'AuthEmailResetPwdHandler')),
        (r'/club/auth/register/into-league', getattr(auth_email, 'AuthRegisterIntoLeagueXHR')),
        (r'/club/auth/logout', getattr(auth_email, 'AuthLogoutHandler')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
