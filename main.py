#!/usr/bin/env python
import webapp2

from webapp2_extras import routes

URL_MAPPING = [
    routes.RedirectRoute('/', redirect_to='https://www.meetup.com/gdglondon', name='GDG London', strict_slash=True)
]

APP = webapp2.WSGIApplication(URL_MAPPING, debug=False)
