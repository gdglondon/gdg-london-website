import os
import jinja2

from eventbrite import Eventbrite
from google.appengine.ext import db


class Events(db.Model):
    Name = db.TextProperty(required=True)
    Description = db.TextProperty(required=True)
    Url = db.TextProperty(required=True)
    LogoUrl = db.TextProperty(required=True)

    StartDateTime = db.DateTimeProperty(required=True)
    EndDateTime = db.DateTimeProperty(required=True)

class Helper(object):
    def __init__(self, eventbrite_uid, eventbrite_key):
        self.eventbrite_uid = eventbrite_uid
        self.eventbrite = Eventbrite(eventbrite_key)
        self.jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

    def get_events_html(self):
        output = self.eventbrite.get_user_owned_events(id=self.eventbrite_uid)
        events_in_html = []

        for event in output['events']:
            if event['listed'] and event['status'] != 'completed':
                html = self.generate_event_in_html(event)
                events_in_html.append(html)

        return events_in_html

    def generate_event_in_html(self, event):
        template = self.jinja.get_template('templates/event.html')
        return template.render({"event": event})
