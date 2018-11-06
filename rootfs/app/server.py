#!/usr/bin/env python
# encoding: utf-8

import os
import flask
import flask_debugtoolbar
import flask_security.decorators

import models
import utils

app = flask.Flask(__name__)
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
# 一个随机生成的字符串，用于加密 cookies
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'NKXXCtpbc6vyuj9QBIVbtepvfEPJM32')
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

app.debug = os.environ.get('FLASK_ENV') == 'development'

app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'bktU\"X2US2@'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

# 添加 debugtoolbar 调试工具条
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PANELS'] = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_mongoengine.panels.MongoDebugPanel'
]

toolbar = flask_debugtoolbar.DebugToolbarExtension(app)
models.config(app)
flask_security.Security(app, models.UserDatastore)


@app.route('/')
def home():
    return 'ok'


@app.route('/member')
@flask_security.decorators.login_required
def member():
    user = flask_security.core.current_user
    return str(user.id)


@app.route('/movies')
def movies():
    data = utils.fetch_movies()
    if not data:
        return '', 500
    return flask.jsonify(data)


if __name__ == "__main__":
    debug = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
