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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from global_const import *


class FoodeeIndexHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        # club_info
        url = API_DOMAIN + "/api/clubs/" + CLUB_ID
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        data = json_decode(response.body)
        club = data['rs']

        # popular activities
        headers = {"Authorization":"Bearer " + DEFAULT_USER_ID}
        params = {"filter":"club", "club_id":CLUB_ID, "_status":20, "popular":1, "page":1, "limit":6}
        url = url_concat(API_DOMAIN + "/api/activities", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got get_activities response.body=[%r]", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        populars = rs['data']

        # popular activities
        headers = {"Authorization":"Bearer " + DEFAULT_USER_ID}
        params = {"filter":"club", "club_id":CLUB_ID, "_status":20, "page":1, "limit":16}
        url = url_concat(API_DOMAIN + "/api/activities", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET", headers=headers)
        logging.info("got get_activities response.body=[%r]", response.body)
        data = json_decode(response.body)
        rs = data['rs']
        activities = rs['data']

        self.render('foodee/index.html',
                club=club,
                populars=populars,
                activities = activities)
