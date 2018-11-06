#!/usr/bin/env python
# encoding: utf-8

import models

users = []

def setup():
    users.append(models.User.objects.create())
