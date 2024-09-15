---
title: "Spiderweb: the Tiny Web Framework"
date: 2024-09-03T16:26:04-04:00
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

I named my little pet project [**Spiderweb**][spiderweb] (a web framework just large enough for a spider), and I sent it off to some friends to get feedback on what I was doing well and what wasn't going well. Out of that feedback, I got two feature requests ([Django-style route declaration][dsrd] and [form validation with Pydantic][pydantic]), so I got that figured out and kept building. Though I'd been putting it off, there was a specific thing that I wanted to make sure I had: [gunicorn support][gunicorn]. Gunicorn is the standard runner for production software for pretty much every project I've ever worked on ([shoutouts to uWSGI though][uwsgi]), so ensuring that my baby framework could interact with it was paramount. 

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

All of the Response classes have a `.render()` function that builds the response into something that can be returned to the browser. This has made extending the Response types with your own very easy, and I'm very happy with how it all came together!

# Stuff I Learned

## Security, Databases, & Other Fun Tricks

Not everything was happiness and rainbows; the internet is a dangerous place, after all. Any framework that accepts POST request also needs to be able to protect against [Cross-Site Request Forgery (CSRF)][csrf], which required a lot more research than I had expected. I implemented a naïve version when building the first version of Spiderweb, only to have a coworker point out that my implementation was essentially a complete failure at what it was supposed to do.

Hilarious.

Implementing it properly involved first adding in database support so that I could build the session middleware, then finally re-implementing CSRF correctly. For database support, I ended up going with [`peewee`][peewee], a Python-based [Object Relational Mapper (ORM)][orm] for interacting with different common databases like SQLite and Postgres.

{{< admonition type=note title="The Best ORM" >}}
The best ORM, by far, is actually the one built into Django. Called simply "the Django ORM", this system of interacting with databases is incredibly solid, flexible, and takes the idea of "if you can't model your query with it, there's a bug" to extremes.

However, the ORM is built into Django in such a way that it cannot be easily extricated. It is [technically possible to run the ORM as a standalone project](https://forum.djangoproject.com/t/django-orm-as-a-standalone-library/4971), but it would require downloading the entirety of the Django web framework while using Spiderweb, which definitely [enters the territory of "...but why?"](https://github.com/itsthejoker/spiderdjango).

{{< /admonition >}}

After rebuilding CSRF protection the proper way, I moved on to another security feature that is often an afterthought for other systems (until it's suddenly very much needed): [Cross-Origin Resource Sharing (CORS)][cors], a vital part of keeping users safe while allowing for larger and more distributed projects. Though it had been my plan from the beginning to implement everything myself and put my own spin on things, I admitted defeat here; the consequences of having a poor implementation here were too high. I turned to [django-cors-headers][django_cors], a project started in 2013 that has been a trusted staple of many production jobs that I've worked on over the years.

Translating `django-cors-headers` into the language of Spiderweb wasn't an easy task, but it did help me better to understand some of the intricacies of the security layer and, in porting the tests that accompany it to make sure I translated it correctly, I discovered several other small bugs in Spiderweb itself that I was able to fix. Roughly 1/3rd of the total development time went into CORS and CSRF protection alone.

## Flexibility in Odd Places

As Spiderweb grew, I was continually surprised by how much I could actually implement in the middleware layer. By extension, I was equally surprised with how much logic didn't actually have to be hard-coded into the framework. As both my coworkers and I floated ideas, I kept thinking, "_where would this go... can I put it in middleware? I think I can!_". Ensuring Spiderweb had extensive (and clear) middleware support means that not only can features be turned on and off at will, but also that new features are very easy for the end user to write for their own personal applications.

I've always known that middleware was powerful, but the sheer amount that it could handle definitely surprised me. I'm very much looking forward to seeing other options for middleware if anyone ends up writing some!

## Takeaways

In working on Spiderweb, there were a lot of surprises and interesting rabbit holes that I went down while working on the entire system. There were times where I was working on different pieces and thought "wait, it would be really nice if..." or, when working on the documentation, I would start to document a function that seemed like it should be there because it made logical sense to be there (like `app.reverse()` for [getting the urls from the name of the route][app_reverse]). In no particular order, these are some of the things that stood out to me while finishing this project.

### Zen of Python vs Ease of Use

The [Zen of Python][zen] says, among other things:

> There should be one-- and preferably only one --obvious way to do it.[^dashes]

When starting on Spiderweb, I had a very specific idea of how I wanted the framework to be used, but I found multiple areas where it just made logical sense to have different ways of achieving the same goal for ease of use. Different situations called for different uses, which is why Spiderweb ended up with [three different ways to set up routes][spiderweb_routes]. I have a preference, but therre's no need to force a preference onto situations where it makes less sense, especially as applications grow.

### Sometimes Python Magic really is the easiest way

In spending years working with Django, there are some things that I have always simply ascribed to "Django Magic". Python has its own forms of magic, but the idea that there were some design decisions that just needed to be memorized was always a little annoying. In working on Spiderweb, there were several places where I intuitively leaned on either more obscure or "maybe not quite good practices" areas of Python to accomplish what I needed — for example, finding the base path of the script calling Spiderweb is done by inspecting the call stack and variables in a URL are cast to their final types by building class names and querying `globals()`. This likely seems... questionable... to the outside viewer, but they are decisions that made the most sense at the time and were easy to quickly implement.

That's not to say that these two are examples that should stay in the framework as time goes on; if I end up continuing to support and extend Spiderweb, there are some definite areas for improvement, and these would likely get some intense scrutiny early on. Like many instances of "Django Magic", I'm sure that they're just what made sense at the time as opposed to a focus on the proper way to approach the problem.

### Having Fun is Fun

With many projects, this one included, there is a certain 'slump' period that happens towards the end. So much work has been completed, but it feels like there's so much left to do... and more projects than not die in this stage. With Spiderweb though, I tried to focus on the parts of building that I genuinely found fun to keep me going.

In this case, I really enjoyed working on the middleware; expanding the framework's capabilities in such a modular way was very exciting, and it became almost a game with myself to see how far I could push the functionality without changing anything in the core server. Having this area that I could come back to was incredibly helpful in keeping me moving and focused.

So, in the words of my partner as we talked about what I learned while working on Spiderweb... "fun is fun!"

## Closing

If any of this looks interesting, I encourage you to checkout [Spiderweb][spiderweb] and see if it's the framework for your next project (or if it's just worth tinkering with). If you find some issues, let me know! It's essentially a toy, but like any creator, I'm dying to know what my creation is capable of. May it serve your requests as well as it has served mine!

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
[django_cors]: https://github.com/adamchainz/django-cors-headers/
[csrf]: https://owasp.org/www-community/attacks/csrf
[peewee]: https://docs.peewee-orm.com/en/latest/peewee/quickstart.html
[orm]: https://stackoverflow.com/a/1279678
[cors]: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
[spiderdjango]: https://example.com

[spiderweb]: https://itsthejoker.github.io/spiderweb
[spiderweb_qs]: https://itsthejoker.github.io/spiderweb/#/quickstart
[spiderweb_routes]: https://itsthejoker.github.io/spiderweb/#/routes
[dsrd]: https://itsthejoker.github.io/spiderweb/#/routes?id=during-instantiation
[pydantic]: https://itsthejoker.github.io/spiderweb/#/middleware/pydantic
[app_reverse]:https://itsthejoker.github.io/spiderweb/#/routes?id=finding-routes-again
[zen]: https://en.wikipedia.org/wiki/Zen_of_Python
[dashes]: https://bugs.python.org/issue3364

<!-- footnotes -->

[^almost]:
    I almost made it. All of the core functionality is my own work, but I leaned on [the shoulders of giants][django_cors] for implementing [CORS (Cross-Origin Resource Sharing)][cors], as it's really something I did not want to screw up.

[^dashes]:
    The formatting of the dashes is specifically different as an illustration of there being different ways to format Python code. It's included [as an Easter egg by the author][dashes].