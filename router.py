# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.auth import auth_email
from foo.portal import quicktravel
from foo.portal import foodee
from foo.portal import story
from foo.portal import verb


def map():

    config = [

        # homepage
        (r'/', getattr(quicktravel, 'QuickTravelIndexHandler')),
        (r'/foodee', getattr(foodee, 'FoodeeIndexHandler')),
        (r'/story', getattr(story, 'StoryIndexHandler')),
        (r'/story/single', getattr(story, 'StorySingleHandler')),
        (r'/verb', getattr(verb, 'VerbIndexHandler')),
        (r'/verb/single', getattr(verb, 'VerbSingleHandler')),
        (r'/verb/category', getattr(verb, 'VerbCategoryHandler')),

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
