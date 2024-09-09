---
title: "Spiderweb: the Tiny Web Framework"
date: 2024-09-03T16:26:04-04:00
draft: true
summary: "I realized that, though it's my day job to use them, I don't know how web frameworks work. So I wrote one."
categories:
  - projects
  - python
tags:
  - python
  - spiderweb
  - learning
---

## Dangers Lurk in the Depths of Learning

As a professional web developer focusing on arcane uses of [Django][django] (and others) for arcane purposes, it occurred to me a little while ago that I didn't actually know how a web framework _worked_.

> So I built one.

This is that story (and lessons learned).

---

## Background

For almost a decade, I have a made a living of weaving websites and apps into existence with Django. I've used it in lots of different contexts: 

- the login experience for USA TODAY
- moving millions of dollars a day to get clients paid on time
- [FilamentColors.xyz][fc], my website for comparing different colors of 3D-printing filaments

...just to name a few. It's such a flexible tool that I never feel that I need to reach for anything else; if there's functionality that it doesn't have built-in, then usually the answer is that either "it actually _is_ built in and I just haven't found it yet" or "someone else has already written it and it's just one install command away". I've written several extensions for Django over the years (rarely ones that see the light of day outside of a corporation), and if I can say anything about the building experience, it's that It Just Works:tm:.

Since my job is building websites (and other cool stuff, but mostly websites), I have to know a lot about my frameworks of choice, but I realized that I didn't really know how it all actually _worked_. How does routing route? What does the request _really_ look like? How does capturing variables from a URL without requiring the user to write regex work? Sure, I _could_ just crack open Django and Flask to see how the sausage is made... or I could just build it myself and learn while I went.

## The Ground Rules

There were only a handful of actual 'rules' that I set for myself. They were, in no particular order:

- write as much as possible on my own — no looking at existing code[^almost]
- take parts I liked about both Django and Flask and merge them together
- be easy to configure
- learn a lot

For the parts that I liked, I had a list of features in mind that I wanted my framework to have (mostly because I wanted to know how they worked):

- Flask's `@app.route()` decorator for route assignments
- URLs with variables in them
- Middleware
- Sessions
- gunicorn support
- database support

It's important to have goals, ya know? So... Python has a [simple HTTP webserver built in][simpleserver]. Could I just subclass that and start expanding on it?

{{< image src="/gifs/my-gut-says-maybe.gif" alt="A gif from _Futurama_ showing a one-shot character saying 'all I know is that my gut says: maybe'." caption="I frequently find myself agreeing with this guy." >}}

## The Framework Begins

The answer is, surprisingly, "yes!", and I eagerly started building. A few days later, I had some functionality I was proud of:

- user-writable views
- mapping routes (URLs) to views
- properly parsing URLs with variables in them
- `GET` and `POST` requests
- HTML template rendering
- HTTP redirects
- basic middleware for handling requests and responses

I named my little pet project [**Spiderweb**][spiderweb] (a web framework just large enough for a spider), and I sent it off to some friends to get feedback on what I was doing well and what wasn't going well. Out of that feedback, I got two feature requests ([Django-style route declaration][dsrd] and [form validation with Pydantic][pydantic]), so I got  figured out and kept building. Though I'd been putting it off, there was a specific thing that I wanted to make sure I had: [gunicorn support][gunicorn]. Gunicorn is the standard runner for production software for pretty much every project I've ever worked on ([shoutouts to uWSGI though][uwsgi]), so ensuring that my baby framework could interact with it was paramount. 

Gunicorn uses a system called [WSGI][wsgi] (Web Server Gateway Interface) to communicate, so I launched into getting my little framework to speak it. And after poking at it for a while, I had a horrifying realization: there is no way to directly translate `SimpleHTTPServer` to WSGI.

When I started this whole adventure, I thought "you know, the WSGI standard has been around forever, so it's probably not an issue. How hard can this be?" The WSGI standard has indeed been around [since 2003][pep-0333] — which in computing years is essentially forever — but what I'd failed to take into account is that `SimpleHTTPServer` has been around _foreverer_.

{{< image src="/images/basehttpserver_first_commit.png" alt="A screenshot of the first ever commit for BaseHTTPServer, showing August 3rd, 1995 by Guido Van Rossum" caption="For those keeping track at home, this is part of Python 1.3." >}}

## Spiderweb

Frustrated, I opened a new file and got writing. Starting from a [minimal viable example][minimal_wsgi_example] of what serving a WSGI application looks like, I reworked all of my logic to fit into this new paradigm, then began to extend. More middleware capabilities came first, then session middleware (and database support), then CSRF middleware, custom error routes, HTML templates, cookies, and most importantly, gunicorn support! Keeping a connection to `SimpleHTTPServer` let me keep an "insecure dev server" for doing local work, and some careful work in the documentation and examples meant that the dev server and gunicorn could both be used at the same time without changing the code.

For folks who have experience with building websites in Python, it should feel pretty familiar:

```python
from spiderweb import SpiderwebRouter
from spiderweb.response import HttpResponse

app = SpiderwebRouter()

@app.route("/")
def index(request):
    return HttpResponse("HELLO, WORLD!")

if __name__ == "__main__":
    app.start()
```

Running the file will result in a default server being created on `http://localhost:8000`, and navigating there in your browser of choice should show "HELLO WORLD" as the only content.

{{< admonition type=info title="Docs!" >}}
Since this post is more about writing Spiderweb more than using it, you can [check out the code above and more at the docs](https://itsthejoker.github.io/spiderweb/#/quickstart)! <!-- link shortcut won't render here :( -->
{{< /admonition >}}

When I was thinking about what I wanted the user experience of views to look like, I made a specific decision that would impact a surprising number of things: a view should not return _data_ (e.g. a string or a dict) but should instead return an explicit intent (with data) from the user of what they expect the framework to do. Some frameworks I've used over the years make assumptions about what exactly the user wants — for example, a returning a dict must mean they want a JSON response — and I think that's kinda silly. Sending data back to the browser should be a deliberate action, and the form that it takes should also be deliberate.

This splits the overall lifecycle of an HTTP request into three parts: the Request, the View, and the Response. These three parts have a total of five states:

1. Browser creates a `Request`
1. All middleware that can do so processes the `Request` object
1. User-created View receives the `Request` and returns a `Response`
1. All middleware that can do so processes the `Response` object
1. Spiderweb renders the finished `Response` and sends it to the browser

I ended up settling on five different responses, with each one automatically setting the correct headers for you (but can be overridden easily):

- `HttpResponse`
  - This is the base response class, and it takes in text that is directly rendered.
- `JsonResponse`
- `TemplateResponse`
  - Takes in either a path to a Jinja template file or a string template, then renders it with optional context data.
- `RedirectResponse`
  - Takes in the path you want to redirect to, then tells the browser to go there instead.
- `FileReponse`
  - Sending files can be kind of a pain, and I realized when working with the dev server that it needed to be able to serve its own static files. The `FileResponse` is mostly for internal use, but is certainly available for others if they need it or want to use it.
  {{< admonition type=tip title="" >}}
  Funnily enough, implementing `FileResponse` was where I realized why [a notice that I'd seen before](https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#django.contrib.staticfiles.views.serve) from the Django documentation about not serving static files via the framework was actually there. To properly serve a file, not only does the request have to go through the entirety of the middleware stack twice (once for the request and once for the response), it probably is also insecure just by nature of it existing.

  So, like... maybe don't do that with Spiderweb either.
  {{< /admonition >}} 



<!-- links -->

[django]: https://www.djangoproject.com/
[fc]: https://filamentcolors.xyz?ref=itsthejoker.github.io
[simpleserver]: https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler
[gunicorn]: https://gunicorn.org/
[uwsgi]: https://uwsgi-docs.readthedocs.io/en/latest/
[wsgi]: https://wsgi.readthedocs.io/en/latest/index.html
[pep-0333]: https://peps.python.org/pep-0333/
[minimal_wsgi_example]: https://wsgi.tutorial.codepoint.net/application-interface
[python1_4]: https://www.python.org/doc/versions/
[cors]: https://github.com/adamchainz/django-cors-headers/

[spiderweb]: https://itsthejoker.github.io/spiderweb
[spiderweb_qs]: https://itsthejoker.github.io/spiderweb/#/quickstart
[dsrd]: https://itsthejoker.github.io/spiderweb/#/routes?id=during-instantiation
[pydantic]: https://itsthejoker.github.io/spiderweb/#/middleware/pydantic

<!-- footnotes -->

[^almost]:
    I almost made it. All of the core functionality is my own work, but I leaned on [the shoulders of giants][cors] for implementing CORS (Cross-Origin Resource Sharing), as it's really something I did not want to screw up.
