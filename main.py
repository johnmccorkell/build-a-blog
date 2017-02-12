import webapp2
import jinja2
import os
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Entry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):

    def render_base(self, title="", content="", error=""):
        entries=db.GqlQuery("SELECT * from Entry ORDER BY created DESC LIMIT 5")
        self.render("base.html", title=title, content=content, error=error, entries=entries)

    def get(self):
        self.render_base()

    def post(self):
        title=self.request.get("title")
        content=self.request.get("content")

        if title and content:
            a=Entry(title=title, content=content)
            a.put()
            self.redirect("/")
        else:
            error="Need both title and content"
            self.render_base(title, content, error=error)


class NewPost(Handler):


    def get(self, title="", content="", error=""):
        self.render("newpost.html")


    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")


        if title and content:
            a=Entry(title=title, content=content)
            a.put()
            self.redirect("/")
        else:
            error="Need both title and content"
            self.render("newpost.html",title=title, content=content, error=error)





app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
