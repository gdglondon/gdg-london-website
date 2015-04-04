import datetime
import os
import jinja2
import json
import urllib2

from google.appengine.ext import db
from google.appengine.api import memcache


class GooglePlusPosts(db.Model):
    PostTimestamp = db.DateTimeProperty(required=True)
    PostJson = db.TextProperty(required=True)
    LastUpdated = db.DateTimeProperty(auto_now_add=True)


class Helper(object):
    def __init__(self, gplus_page_id, gplus_api_key):
        self.profile_id = gplus_page_id
        self.api_key = gplus_api_key
        self.jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

    def store_google_plus_posts(self):
        url = "https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s" % (
            self.profile_id, self.api_key)

        response = urllib2.urlopen(url, timeout=20).read()
        json_response = json.loads(response)

        for item in json_response["items"]:
            post_timestamp = datetime.datetime.strptime(item["updated"][:-5], "%Y-%m-%dT%H:%M:%S")
            GooglePlusPosts(key_name=item["id"], PostJson=unicode(json.dumps(item), 'utf-8'),
                            PostTimestamp=post_timestamp).save()

    def get_google_plus_posts_html(self):
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

        for i, post in enumerate(posts):
            post_in_html = self.generate_html_google_plus_post(post, i)
            posts_in_html.append(post_in_html)

        return posts_in_html

    def generate_html_google_plus_post(self, post, i):
        template = self.jinja.get_template('templates/googlepluspost.html')
        return template.render({"post": post, "i": i})
