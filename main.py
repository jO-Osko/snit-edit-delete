#!/usr/bin/env python

import os

import jinja2
import webapp2

from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class IndexHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class RezultatHandler(BaseHandler):
    def post(self):
        sporocilo = self.request.get("vnos")

        sporocilo_v_bazi = Sporocilo(besedilo=sporocilo)
        sporocilo_v_bazi.put()

        return self.write("Vpisal si: " + sporocilo)


class SeznamSporocilHandler(BaseHandler):
    def get(self):

        vsa_sporocila = Sporocilo.query().fetch()

        params = {"sporocila": vsa_sporocila}

        return self.render_template("vsa_sprocila.html", params=params)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {"sporocilo": sporocilo}

        return self.render_template("posamezno_sporocilo.html",
                                    params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', IndexHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/vsa_sporocila', SeznamSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\\d+>', PosameznoSporociloHandler)
], debug=True)
