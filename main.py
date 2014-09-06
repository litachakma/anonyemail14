#!/usr/local/bin/python2.7
    
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        username = 'Lumbini'
        
        template_values = {
            'username': username
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        # self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
