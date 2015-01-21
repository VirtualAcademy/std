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
import jinja2
import webapp2

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

class Rot13(object):
    import string

    alpha = string.ascii_letters
    cph_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',
             5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
             10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
             15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't',
             20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}

    def __init__(self, text):
        self.shift = 13
        self.text = text

    def get_index(self,ltr):
        return self.alpha.index(ltr)

    def c_cipher(self,text):
        self.cph_wrd = str()
        for letter in text:
            if not letter in self.alpha:
                self.cph_wrd += letter
                continue
            letter_index = self.get_index(letter.lower())
            cph_index = letter_index + self.shift
            if cph_index > 25:
                cph_index = (cph_index % 25) - 1

            if letter.isupper():
                self.cph_wrd += self.cph_dict[cph_index].upper()
            else:
                self.cph_wrd += self.cph_dict[cph_index]
        return self.cph_wrd

    def rot13(self):
        txt = self.c_cipher(self.text)
        return txt

app = webapp2.WSGIApplication([('/', MainPage)
                              ], debug=True)
