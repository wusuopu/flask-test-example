#!/usr/bin/env python
# encoding: utf-8

import requests


def fetch_movies():
    try:
        url = 'http://api.douban.com/v2/movie/top250?start=0&count=10'
        res = requests.get(url, timeout=5)
        return res.json()
    except Exception as e:
        return None
