#!/usr/local/bin/python2.7
    
import os
import urllib
import logging
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from google.appengine.api import mail

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

class TermsPage(webapp2.RequestHandler):
    def get(self):
        
        terms = 'Terms and  Conditions goes here'
        template_values = {
            'terms': terms
        }

        template = JINJA_ENVIRONMENT.get_template('terms.html')
        # self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(template_values))


class SendEmail(webapp2.RequestHandler):
    def post(self):
        
        # cgi.escape(self.request.get('content'))

        to = cgi.escape(self.request.get('to'))
        message = mail.EmailMessage(sender=cgi.escape(self.request.get('from')),
                            subject=cgi.escape(self.request.get('subject')))

        message.to = to
        message.body = cgi.escape(self.request.get('message'))

        message.send()
        self.response.write("Sent email to: " + to)        



app = webapp2.WSGIApplication([
    ('/', MainPage),
     ('/terms', TermsPage),
     ('/sendmail', SendEmail),
], debug=True)


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("================================")
        logging.info("Received a mail_message from: " + mail_message.sender)
        logging.info("The email subject: " + mail_message.subject)
       
        try:
            logging.info("The email was addressed to: " + str.join(mail_message.to, ', '))
            logging.info("The email was CC-ed to: " + str.join(mail_message.cc, ', '))
        except exceptions.AttributeError :
            logging.info("The email has no CC-ed recipients")

        try:
            logging.info("The email was send on: " + str(mail_message.date))
        except exceptions.AttributeError :
            logging.info("The email has no send date specified!!!")

        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            decoded_html = body.decode()
            logging.info("content_type: " + content_type)
            logging.info("decoded_html: " + decoded_html)

mailer = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)