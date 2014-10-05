#!/usr/bin/env python
import os
import webapp2
import urllib2
import json
import pickle
import cgi

from webapp2_extras import *
from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.api import memcache
from webapp2_extras import routes
import jinja2
import datetime
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

with open(os.path.join(os.path.dirname(__file__), "api.json"), "r") as f:
  APIKEY = json.load(f)

if 'Development' in os.environ['SERVER_SOFTWARE']:
	siteURL = 'http://localhost:8080/'
	siteDomain = 'localhost'
else:
	siteURL = 'http://www.gdg-london.com/'
	siteDomain = 'www.gdg-london.com'

class GooglePlusPosts(db.Model):
  PostTimestamp = db.DateTimeProperty(required=True)
  PostJson = db.TextProperty(required=True)
  LastUpdated = db.DateTimeProperty(auto_now_add=True)

class Helper:
  def __init__(self):
    self.profileId = "+Gdg-london"
    self.apiKey = APIKEY

  def storeGooglePlusPosts(self):
    apiendpoint = "https://www.googleapis.com/plus/v1/people/" \
                  + self.profileId + \
                  "/activities/public?key=" + self.apiKey

    response = urllib2.urlopen(apiendpoint, timeout=20).read()
    jsonResponse = json.loads(response)
    for item in jsonResponse["items"]:
        postTimestamp = datetime.datetime.strptime(item["updated"][:-5], "%Y-%m-%dT%H:%M:%S")
        GooglePlusPosts(key_name=item["id"], PostJson=unicode(json.dumps(item), 'utf-8'),
                        PostTimestamp=postTimestamp).save()

  def getGooglePlusPosts(self):
    #connect datastore and call function to get html for each post, do exception handling here
    response = memcache.get("GooglePlusPosts")
    if not response:
        q = db.GqlQuery("SELECT * FROM GooglePlusPosts ORDER BY PostTimestamp DESC LIMIT 20")
        posts = []
        for item in q:
            posts.append(json.loads(item.PostJson))
        response = json.dumps(posts)
        memcache.add("GooglePlusPosts", response, 60)
    postsInHTML = []
    posts = json.loads(response)
    for i in range(0,len(posts)):
      post = posts[i]
      #try:
      postinHTML = self.generateHTMLGooglePlusPost(post, i)
      postsInHTML.append(postinHTML)
      #except:
      postsInHTML.append("<!-- Failed to parse " + post["id"] + "-->")
    return postsInHTML

  def generateHTMLGooglePlusPost(self, post, i ):
    ''' returns HTML for Google+ post and exception return None '''
    template = jinja_environment.get_template('templates/googlepluspost.html')
    return template.render({"post": post, "i": i})


class CronHandler(webapp2.RequestHandler):
  def get(self):
    Helper().storeGooglePlusPosts()

class GDGHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    # Generate Google+ post
    posts = Helper().getGooglePlusPosts()
    template = jinja_environment.get_template('templates/index.html')
    self.response.write(template.render({"posts": posts}))

class DevfestHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.set_status('301',message=None)
    self.redirect(siteURL + "devfest/")

URL_Mapping = [
  webapp2.Route('/', handler=GDGHandler, name='GDG London'), 
  webapp2.Route('/devfest', handler=DevfestHandler, name='Devfest'),
  webapp2.Route('/cron/gplus', handler=CronHandler)
]

app = webapp2.WSGIApplication(URL_Mapping, debug=False)