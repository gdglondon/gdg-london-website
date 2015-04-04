#!/usr/bin/env python
import os
import webapp2
import jinja2
import json

import google_plus
from webapp2_extras import routes

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    CONFIG = json.load(f)

class CronHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

        self.gplus = google_plus.Helper(
            CONFIG['google_plus_page_id'], CONFIG['google_plus_key'])

    def get(self):
        self.gplus.store_google_plus_posts()
        self.response.write('')

class MainHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

        self.jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

        self.gplus = google_plus.Helper(
            CONFIG['google_plus_page_id'], CONFIG['google_plus_key'])

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = self.jinja.get_template('templates/index.html')

        output = template.render({
            "posts": self.gplus.get_google_plus_posts_html()
        })

        self.response.write(output)

URL_MAPPING = [
    webapp2.Route('/', handler=MainHandler, name='GDG London'),
    routes.RedirectRoute('/devfest', redirect_to='http://devfest.gdg-london.com',
                         name='Devfest', strict_slash=True),
    webapp2.Route('/cron/gplus', handler=CronHandler)
]

APP = webapp2.WSGIApplication(URL_MAPPING, debug=False)
