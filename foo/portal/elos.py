#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 planc2c.com
# thomas@time2box.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import uuid
import smtplib
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from global_const import *


class ElosHomeHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        self.redirect("/elos/clubs/"+CLUB_ID+"/services")


class ElosClubIndexHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        # recently articles(最近文章)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"all", "idx":0, "limit":10}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        articles = rs['rs']
        for article in articles:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/index.html',
                is_login=is_login,
                club=club,
                categories=categories,
                articles=articles,
                populars=populars)


class ElosBlogIndexHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        # recently articles(最近文章)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"all", "idx":0, "limit":10}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        articles = rs['rs']
        for article in articles:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-index.html',
                is_login=is_login,
                club=club,
                categories=categories,
                articles=articles,
                populars=populars)


class ElosBlogCategoryHandler(tornado.web.RequestHandler):
    def get(self, club_id, category_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/categories/"+category_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        category = rs['rs']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        # recently articles(最近文章)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":category_id, "idx":0, "limit":10}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        articles = rs['rs']
        for article in articles:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":CLUB_ID, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-category.html',
                club=club,
                is_login=is_login,
                category=category,
                categories=categories,
                articles=articles,
                populars=populars)


class ElosBlogPostHandler(tornado.web.RequestHandler):
    def get(self, club_id, article_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        article_info = rs['rs']

        html = article_info['paragraphs']
        # 为图片延迟加载准备数据
        # <img alt="" src="http://bighorn.b0.upaiyun.com/blog/2016/11/2/758f7478-d406-4f2e-9566-306a963fb979" />
        # <img data-original="真实图片" src="占位符图片">
        ptn="(<img src=\"http[s]*://[\w\.\/\-]+\" />)"
        img_ptn = re.compile(ptn)
        imgs = img_ptn.findall(html)
        for img in imgs:
            logging.info("got img %r", img)
            ptn="<img src=\"(http[s]*://[\w\.\/\-]+)\" />"
            url_ptn = re.compile(ptn)
            urls = url_ptn.findall(html)
            url = urls[0]
            logging.info("got url %r", url)
            #html = html.replace(img, "<img class=\"lazy\" data-original=\""+url+"\" src=\"/static/images/weui.png\" width=\"100%\" height=\"480\" />")
            html = html.replace(img, "<img width='100%' src='"+url+"' />")
        logging.info("got html %r", html)
        article_info['paragraphs'] = html
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-post.html',
                club=club,
                is_login=is_login,
                categories=categories,
                article=article_info,
                populars=populars)


class ElosBlogPostEditHandler(tornado.web.RequestHandler):
    def get(self, club_id, article_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        article_info = rs['rs']

        html = article_info['paragraphs']
        # 为图片延迟加载准备数据
        # <img alt="" src="http://bighorn.b0.upaiyun.com/blog/2016/11/2/758f7478-d406-4f2e-9566-306a963fb979" />
        # <img data-original="真实图片" src="占位符图片">
        ptn="(<img src=\"http[s]*://[\w\.\/\-]+\" />)"
        img_ptn = re.compile(ptn)
        imgs = img_ptn.findall(html)
        for img in imgs:
            logging.info("got img %r", img)
            ptn="<img src=\"(http[s]*://[\w\.\/\-]+)\" />"
            url_ptn = re.compile(ptn)
            urls = url_ptn.findall(html)
            url = urls[0]
            logging.info("got url %r", url)
            #html = html.replace(img, "<img class=\"lazy\" data-original=\""+url+"\" src=\"/static/images/weui.png\" width=\"100%\" height=\"480\" />")
            html = html.replace(img, "<img width='100%' src='"+url+"' />")
        logging.info("got html %r", html)
        article_info['paragraphs'] = html
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-post-edit.html',
                club=club,
                is_login=is_login,
                categories=categories,
                article=article_info,
                populars=populars)


class ElosBlogPostEditInlineHandler(tornado.web.RequestHandler):
    def get(self, club_id, article_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        article_info = rs['rs']

        html = article_info['paragraphs']
        # 为图片延迟加载准备数据
        # <img alt="" src="http://bighorn.b0.upaiyun.com/blog/2016/11/2/758f7478-d406-4f2e-9566-306a963fb979" />
        # <img data-original="真实图片" src="占位符图片">
        ptn="(<img src=\"http[s]*://[\w\.\/\-]+\" />)"
        img_ptn = re.compile(ptn)
        imgs = img_ptn.findall(html)
        for img in imgs:
            logging.info("got img %r", img)
            ptn="<img src=\"(http[s]*://[\w\.\/\-]+)\" />"
            url_ptn = re.compile(ptn)
            urls = url_ptn.findall(html)
            url = urls[0]
            logging.info("got url %r", url)
            #html = html.replace(img, "<img class=\"lazy\" data-original=\""+url+"\" src=\"/static/images/weui.png\" width=\"100%\" height=\"480\" />")
            html = html.replace(img, "<img width='100%' src='"+url+"' />")
        logging.info("got html %r", html)
        article_info['paragraphs'] = html
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-post-edit-inline.html',
                club=club,
                is_login=is_login,
                categories=categories,
                article=article_info,
                populars=populars)


class ElosBlogPostEditSyntaxhighlighterHandler(tornado.web.RequestHandler):
    def get(self, club_id, article_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        article_info = rs['rs']

        html = article_info['paragraphs']
        # 为图片延迟加载准备数据
        # <img alt="" src="http://bighorn.b0.upaiyun.com/blog/2016/11/2/758f7478-d406-4f2e-9566-306a963fb979" />
        # <img data-original="真实图片" src="占位符图片">
        ptn="(<img src=\"http[s]*://[\w\.\/\-]+\" />)"
        img_ptn = re.compile(ptn)
        imgs = img_ptn.findall(html)
        for img in imgs:
            logging.info("got img %r", img)
            ptn="<img src=\"(http[s]*://[\w\.\/\-]+)\" />"
            url_ptn = re.compile(ptn)
            urls = url_ptn.findall(html)
            url = urls[0]
            logging.info("got url %r", url)
            #html = html.replace(img, "<img class=\"lazy\" data-original=\""+url+"\" src=\"/static/images/weui.png\" width=\"100%\" height=\"480\" />")
            html = html.replace(img, "<img width='100%' src='"+url+"' />")
        logging.info("got html %r", html)
        article_info['paragraphs'] = html
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # Tornado模板引擎一直有一个坑，有时候你可能觉得并不影响正常使用，但使用代码格式化控制就不行了：模板会去掉每行前后的空格。
        # 模板文件不为.html或.js后缀，可以为.htm或.tpl等。
        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-post-edit-syntaxhighlighter.htm',
                club=club,
                is_login=is_login,
                categories=categories,
                article=article_info,
                populars=populars)


class ElosBlogPostEditCustomerButtonHandler(tornado.web.RequestHandler):
    def get(self, club_id, article_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        url = "http://api.7x24hs.com/api/articles/"+article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        article_info = rs['rs']

        html = article_info['paragraphs']
        # 为图片延迟加载准备数据
        # <img alt="" src="http://bighorn.b0.upaiyun.com/blog/2016/11/2/758f7478-d406-4f2e-9566-306a963fb979" />
        # <img data-original="真实图片" src="占位符图片">
        ptn="(<img src=\"http[s]*://[\w\.\/\-]+\" />)"
        img_ptn = re.compile(ptn)
        imgs = img_ptn.findall(html)
        for img in imgs:
            logging.info("got img %r", img)
            ptn="<img src=\"(http[s]*://[\w\.\/\-]+)\" />"
            url_ptn = re.compile(ptn)
            urls = url_ptn.findall(html)
            url = urls[0]
            logging.info("got url %r", url)
            #html = html.replace(img, "<img class=\"lazy\" data-original=\""+url+"\" src=\"/static/images/weui.png\" width=\"100%\" height=\"480\" />")
            html = html.replace(img, "<img width='100%' src='"+url+"' />")
        logging.info("got html %r", html)
        article_info['paragraphs'] = html
        article_info['publish_time'] = timestamp_friendly_date(article_info['publish_time'])

        # popular(流行)
        params = {"filter":"club", "club_id":club_id, "status":"publish", "category":"3801d62cf73411e69a3c00163e023e51", "idx":0, "limit":3}
        url = url_concat("http://api.7x24hs.com/api/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        populars = rs['rs']
        for article in populars:
            article['publish_time'] = timestamp_friendly_date(article['publish_time'])

        # Tornado模板引擎一直有一个坑，有时候你可能觉得并不影响正常使用，但使用代码格式化控制就不行了：模板会去掉每行前后的空格。
        # 模板文件不为.html或.js后缀，可以为.htm或.tpl等。
        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/blog-post-edit-customer-button.htm',
                club=club,
                is_login=is_login,
                categories=categories,
                article=article_info,
                populars=populars)


class ElosLoginHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/login.html',
                is_login=is_login,
                club=club,
                categories=categories)


class ElosLogoutHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)
        access_token = self.get_secure_cookie("access_token")

        # logout
        url = API_DOMAIN+"/api/auth/tokens"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE", headers={"Authorization":"Bearer "+access_token})
        logging.info("got response %r", response.body)

        self.clear_cookie("access_token")
        self.clear_cookie("expires_at")
        self.clear_cookie("login_next")
        self.clear_cookie("refresh_token")

        self.redirect("/elos/clubs/"+club_id+"/services")


class ElosRegisterHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/register.html',
                club=club,
                is_login=is_login,
                categories=categories)


class ElosContactHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/contact.html',
                club=club,
                is_login=is_login,
                categories=categories)


class ElosAboutHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/about.html',
                club=club,
                is_login=is_login,
                categories=categories)


class ElosServiceHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/services.html',
                club=club,
                is_login=is_login,
                categories=categories)


class ElosPortfolioHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/portfolio.html',
                club=club,
                is_login=is_login,
                categories=categories)


class ElosPortfolioImagesHandler(tornado.web.RequestHandler):
    def get(self, club_id):
        logging.info(self.request)

        url = "http://api.7x24hs.com/api/clubs/"+club_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        club = rs['rs']
        league_id = club['league_id']

        url = "http://api.7x24hs.com/api/leagues/"+league_id+"/categories"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        categories = rs['rs']

        # multimedia
        params = {"filter":"league", "league_id":league_id, "idx":0, "limit":8}
        url = url_concat("http://api.7x24hs.com/api/multimedias", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        rs = json_decode(response.body)
        multimedias = rs['rs']
        for multimedia in multimedias:
            multimedia['publish_time'] = timestamp_friendly_date(multimedia['publish_time'])

        is_login = False
        access_token = self.get_secure_cookie("access_token")
        logging.info("got access_token>>>>> %r",access_token)
        if access_token:
            is_login = True

        self.render('elos/portfolio-images.html',
                is_login=is_login,
                club=club,
                categories=categories,
                multimedias=multimedias)
