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
from foo.portal import elos


def map():

    config = [

        # homepage
        (r'/', getattr(elos, 'ElosHomeHandler')),
        (r'/quicktravel', getattr(quicktravel, 'QuickTravelIndexHandler')),
        (r'/foodee', getattr(foodee, 'FoodeeIndexHandler')),

        (r'/story', getattr(story, 'StoryHomeHandler')),
        (r'/story/clubs/([a-z0-9]*)/index', getattr(story, 'StoryIndexHandler')),
        (r'/story/clubs/([a-z0-9]*)/articles/([a-z0-9]*)', getattr(story, 'StoryArticleHandler')),

        (r'/verb', getattr(verb, 'VerbHomeHandler')),
        (r'/verb/clubs/([a-z0-9]*)/index', getattr(verb, 'VerbClubIndexHandler')),
        (r'/verb/clubs/([a-z0-9]*)/info', getattr(verb, 'VerbClubInfoHandler')),
        (r'/verb/clubs/([a-z0-9]*)/categoies/([a-z0-9]*)', getattr(verb, 'VerbCategoryHandler')),
        (r'/verb/clubs/([a-z0-9]*)/articles/([a-z0-9]*)', getattr(verb, 'VerbArticleHandler')),

        (r'/elos', getattr(elos, 'ElosHomeHandler')),
        (r'/elos/clubs/([a-z0-9]*)/index', getattr(elos, 'ElosClubIndexHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs', getattr(elos, 'ElosBlogIndexHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs/([a-z0-9]*)', getattr(elos, 'ElosBlogPostHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs/([a-z0-9]*)/edit', getattr(elos, 'ElosBlogPostEditHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs/([a-z0-9]*)/edit-inline', getattr(elos, 'ElosBlogPostEditInlineHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs/([a-z0-9]*)/edit-syntaxhighlighter', getattr(elos, 'ElosBlogPostEditSyntaxhighlighterHandler')),
        (r'/elos/clubs/([a-z0-9]*)/blogs/([a-z0-9]*)/edit-customer-button', getattr(elos, 'ElosBlogPostEditCustomerButtonHandler')),
        (r'/elos/clubs/([a-z0-9]*)/categories/([a-z0-9]*)', getattr(elos, 'ElosBlogCategoryHandler')),
        (r'/elos/clubs/([a-z0-9]*)/login', getattr(elos, 'ElosLoginHandler')),
        (r'/elos/clubs/([a-z0-9]*)/register', getattr(elos, 'ElosRegisterHandler')),
        (r'/elos/clubs/([a-z0-9]*)/about', getattr(elos, 'ElosAboutHandler')),
        (r'/elos/clubs/([a-z0-9]*)/contact', getattr(elos, 'ElosContactHandler')),
        (r'/elos/clubs/([a-z0-9]*)/services', getattr(elos, 'ElosServiceHandler')),
        (r'/elos/clubs/([a-z0-9]*)/portfolio', getattr(elos, 'ElosPortfolioHandler')),
        (r'/elos/clubs/([a-z0-9]*)/portfolio-images', getattr(elos, 'ElosPortfolioImagesHandler')),

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
