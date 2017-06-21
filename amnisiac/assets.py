# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css_all = Bundle(
    'libs/bootstrap/dist/css/bootstrap.min.css',
    'libs/jquery-ui/themes/smoothness/jquery-ui.css',
    'libs/select2/dist/css/select2.min.css',
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css'
)

js_common = Bundle(
    'libs/jquery/dist/jquery.min.js',
    'libs/jquery-ui/jquery-ui.min.js',
    'libs/bootstrap/dist/js/bootstrap.min.js',
    "libs/select2/dist/js/select2.full.js",
    'libs/youtube-iframe-api/youtube.iframe-api.js',
    'libs/api/index.js',
    'js/search.js',
    'js/feed.js',
    'js/save.js',
    filters='jsmin',
    output='public/js/common.js'
)



# js_all = Bundle(
#     'libs/jquery/dist/jquery.min.js',
#     'libs/jquery-ui/jquery-ui.min.js',
#     'libs/bootstrap/dist/js/bootstrap.min.js',
#     filters='jsmin',
#     output='public/js/main.js')


# js_search = Bundle(
#     'libs/jquery/dist/jquery.min.js',
#     'libs/jquery-ui/jquery-ui.min.js',
#     'libs/bootstrap/dist/js/bootstrap.min.js',
#     "libs/select2/dist/js/select2.full.js",
#     'search.js',
#     filters='jsmin',
#     output='public/js/save.js')

# js_feed = Bundle(
#     'libs/jquery/dist/jquery.min.js',
#     'libs/jquery-ui/jquery-ui.min.js',
#     'libs/bootstrap/dist/js/bootstrap.min.js',
#     'libs/youtube-iframe-api/youtube.iframe-api.js',
#     'libs/api/index.js',
#     'feed.js',
#     'save.js',
#     filters='jsmin',
#     output='public/js/feed.js')

assets = Environment()

assets.register('js_common', js_common)
assets.register('css_all', css_all)
# assets.register('js_all', js_all)
# assets.register('js_feed', js_feed)
# assets.register('js_search', js_search)
