#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import pytest

os.environ.update({'FLASK_ENV': 'test'})
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

from server import app as App
import fixture


@pytest.fixture
def app():
    return App


@pytest.fixture
def auth_client(client):
    with client.session_transaction() as sess:
        sess['user_id'] = str(fixture.users[0].id)

    yield client
