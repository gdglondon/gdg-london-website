#!/usr/bin/env python
import os
import webapp2
import urllib2
import json
import jinja2
import datetime

from google.appengine.ext import db
from google.appengine.api import memcache
from webapp2_extras import routes


JINJA = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    CONFIG = json.load(f)


class GooglePlusPosts(db.Model):
    PostTimestamp = db.DateTimeProperty(required=True)
    PostJson = db.TextProperty(required=True)
    LastUpdated = db.DateTimeProperty(auto_now_add=True)


class Helper(object):
    def __init__(self):
        self.profile_id = "+Gdg-london"
        self.api_key = CONFIG["google_plus_key"]

    def store_google_plus_posts(self):
        apiendpoint = "https://www.googleapis.com/plus/v1/people/" \
                      + self.profile_id + \
                      "/activities/public?key=" + self.api_key

        response = urllib2.urlopen(apiendpoint, timeout=20).read()
        json_response = json.loads(response)

        for item in json_response["items"]:
            post_timestamp = datetime.datetime.strptime(item["updated"][:-5], "%Y-%m-%dT%H:%M:%S")
            GooglePlusPosts(key_name=item["id"], PostJson=unicode(json.dumps(item), 'utf-8'),
                            PostTimestamp=post_timestamp).save()

def get_google_plus_posts():
    #connect datastore and call function to get html for each post, do exception handling here
    response = memcache.get("GooglePlusPosts")
    if not response:
        query = db.GqlQuery("SELECT * FROM GooglePlusPosts ORDER BY PostTimestamp DESC LIMIT 20")
        posts = []
        for item in query:
            posts.append(json.loads(item.PostJson))
        response = json.dumps(posts)
        memcache.add("GooglePlusPosts", response, 60)
    posts_in_html = []
    posts = json.loads(response)

    for i in range(0, len(posts)):
        post = posts[i]
        #try:
        post_in_html = generate_html_google_plus_post(post, i)
        posts_in_html.append(post_in_html)
        #except:
        posts_in_html.append("<!-- Failed to parse " + post["id"] + "-->")

    return posts_in_html

def generate_html_google_plus_post(post, i):
    ''' returns HTML for Google+ post and exception return None '''
    template = JINJA.get_template('templates/googlepluspost.html')
    return template.render({"post": post, "i": i})

class CronHandler(webapp2.RequestHandler):
    def get(self):
        Helper().store_google_plus_posts()
        self.response.write('')

class GDGHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # Generate Google+ post
        posts = get_google_plus_posts()
        template = JINJA.get_template('templates/index.html')
        self.response.write(template.render({"posts": posts}))

URL_MAPPING = [
    webapp2.Route('/', handler=GDGHandler, name='GDG London'),
    routes.RedirectRoute('/devfest', redirect_to='http://devfest.gdg-london.com',
                         name='Devfest', strict_slash=True),
    webapp2.Route('/cron/gplus', handler=CronHandler)
]

APP = webapp2.WSGIApplication(URL_MAPPING, debug=False)
