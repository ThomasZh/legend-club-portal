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
        (r'/verb', getattr(verb, 'VerbHomeHandler')),
        (r'/verb/clubs/([a-z0-9]*)/index', getattr(verb, 'VerbClubIndexHandler')),
        (r'/verb/clubs/([a-z0-9]*)/info', getattr(verb, 'VerbClubInfoHandler')),
        (r'/verb/clubs/([a-z0-9]*)/categoies/([a-z0-9]*)', getattr(verb, 'VerbCategoryHandler')),
        (r'/verb/clubs/([a-z0-9]*)/articles/([a-z0-9]*)', getattr(verb, 'VerbArticleHandler')),

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
