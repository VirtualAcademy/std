#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import re
import jinja2
import webapp2
from google.appengine.ext import db
from cipher.ciph import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(MainHandler):
    def get(self):
        return self.render('h.html')

    def post(self):
        txt=self.request.get('text')
        text=Rot13(txt)
        return self.render('r.html', value=text.rot13())


class SignupPage(MainHandler):
    def get(self):
        return self.render('signup.html')

    def post(self):
        items = [self.request.get(item) for item in ('username','password','verify','email')] # Get input data from form
        username,password,verify,email = items
        usrvalid = not(self.not_valid_user(username))
        passvalid = not(self.not_valid_user(password))
        passverified = self.verify_pass(password, verify)
        emailvalid = not(self.not_valid_email(email))
        #self.response.out.write({'passverify':{password:passverified},'user':{username:usrvalid},'passvalid':{password:passvalid},'email':{email:emailvalid}})

###     First case all inputs valid
        if usrvalid and passvalid and passverified and emailvalid:
            self.acc = UsersAccounts(users_name=username,users_pass=password,users_email=email)#users_name=self.request.get('username'),users_pass=self.request.get('password'),users_email=self.request.get('email'))
            self.acc.put()
            self.redirect('/welcome?username=%s'%username)
            #if len(outcome)>1:
            #    self.response.out.write('welcome %s' %outcome)#redirect('/welcome')
            #self.acc.put()
            #self.redirect('/welcome')

###     Second case not all inputs are valid
        else:
            error1=None
            error2=None
            mail=None
            verified=None
            if not(emailvalid):
                mail=1
            if not (passvalid):
                error2 = 1
            if not (usrvalid):
                error1=1
            if not (passverified):
                verified=1

            return self.render('signup.html', username=username, password=password, error1=1, error2=1)
            ## Invalid Password and Username
           # if not( usrvalid and passvalid ):
            #    return self.render('signup.html', username=username, password=password, error1=1, error2=1)

            ## Either Invalid Password or Username
            #elif not(self.not_valid_user(username)) or not(self.not_valid_pass(password)):
             #   if not(self.not_valid_user(username)): # Case of invalid username
              #      return self.render('signup.html', error1=1)
               # else:# Case of invalid password
                #    return self.render('signup.html', error2=1)

            ## Password mismatch
            #elif not (password == verify):
             #   return self.render('signup.html',verify=verify, error=[passverified,usrvalid,passvalid,emailvalid])

    def not_valid_user(self,username):
        return not(re.match( r"^[a-zA-Z0-9_-]{3,20}$", username))
        #if len(username.split())>1:
         #   return False
        #return True

    def not_valid_pass(self,passw):
        return not(re.match( r"^.{3,20}$", passw))
        #if len(username.split())>1:

    def verify_pass(self, password, verify):
        if password == '' or verify == '':
            return False
        return password == verify

    def not_valid_email(self, email):
        e_pattern = '^[\S]+@[\S]+\.[\S]+$'
        ecom = re.compile(e_pattern)
        return not(re.match(ecom, email))


class WelcomePage(SignupPage):
    def get(self):
        user = UsersAccounts.all()
        user.order('-period')
        return self.render('wel.html',user=user.get().users_name)


class UsersAccounts(db.Model):
    users_name = db.StringProperty(required=True)
    users_pass = db.StringProperty(required=True)
    users_email = db.StringProperty(required=False)
    period = db.DateTimeProperty(auto_now_add=True)


app = webapp2.WSGIApplication([('/rot13', MainPage),
                               ('/signup',SignupPage),
                               ('/welcome',WelcomePage)
                              ], debug=True)
