#!/usr/bin/env python
# encoding: utf-8

import os

bind = ["0.0.0.0:80"]
timeout = 80
chdir = os.path.dirname(os.path.realpath(__file__))
accesslog = '-'
errorlog = "-"
capture_output = True
daemon = False
pidfile = "/tmp/gunicorn.pid"
loglevel = 'debug' if os.environ.get('FLASK_ENV') == 'development' else 'info'
