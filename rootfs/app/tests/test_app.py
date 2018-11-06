#!/usr/bin/env python
# encoding: utf-8

import sys
import os

os.environ.update({'FLASK_ENV': 'test'})
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

from server import app as App
import flask
import mock
import json
import time
import models
import six.moves
import fixture


def setup_module(module):
    App.testing = True
    fixture.setup()


def teardown_module(module):
    """
    """


def test_home_page(client):
    """
    测试首页
    """
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.data == b'ok'


def test_member_page_without_login(client):
    """
    没有登录则跳转到登录页面
    """
    rv = client.get('/member')
    assert rv.headers['Location'] == 'http://localhost/login?next=%2Fmember'
    assert rv.status_code == 302


def test_member_page_with_login(auth_client):
    """
    已经登录则返回当前用户id
    """
    rv = auth_client.get('/member')
    assert rv.status_code == 200
    assert rv.data.decode('utf8') == str(fixture.users[0].id)
