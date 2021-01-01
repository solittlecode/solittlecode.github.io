#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Tom Howlett'
SITENAME = 'SoLittleCode Blog'
SITEURL = ''

STATIC_PATHS = [
    'images',
    'extra', 
]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},  
    'extra/CNAME': {'path': 'CNAME'},
}

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

THEME = 'themes/slc1'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True