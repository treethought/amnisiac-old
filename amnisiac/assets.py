# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'main.css',
    filters='cssmin',
    output='public/css/common.css'
)

# js = Bundle(
#     'libs/jquery/dist/jquery.js',
#     'libs/bootstrap/dist/js/bootstrap.js',
#     'js/plugins.js',
#     filters='jsmin',
#     output='public/js/common.js'
# )

js_search = Bundle(
    'libs/jquery/dist/jquery.js',
    'libs/jquery-ui/jquery-ui.js',
    "libs/select2/dist/js/select2.full.js",
    'search.js',
    filters='jsmin',
    output='public/js/save.js')

js_feed = Bundle(
    'libs/jquery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/youtube-iframe-api/youtube.iframe-api.js',
    'libs/api/index.js',
    'feed.js',
    'save.js',
    filters='jsmin',
    output='public/js/feed.js')

assets = Environment()

# assets.register('js_all', js)
assets.register('css_all', css)
assets.register('js_feed', js_feed)
assets.register('js_search', js_search)
