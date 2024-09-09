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

As a professional web developer focusing on arcane uses of [Django][django] for arcane purposes, it occurred to me a little while ago that I didn't actually know how a web framework _worked_.

> So I built one.

This is that story (and lessons learned).

---

## Background

For almost a decade, I have a made a living of weaving websites and apps into existence with Django. I've used it in lots of different contexts: the login experience for USA TODAY, moving millions of dollars a day to get clients paid on time, and [my 3D-printing filament website][fc] just to name a few. It's such a flexible tool that I never feel that I need to reach for anything else; if there's functionality that it doesn't have built-in, then usually the answer is that either "it actually _is_ built in and I just haven't found it yet" or "someone else has already written it and it's just one install command away". I've written several extensions for Django over the years (rarely ones that see the light of day outside of a corporation), and if I can say anything about the building experience, it's that It Just Works:tm:.

I've spent a lot of time digging around in Django's internals, and while most of it makes sense, there's a lot of Django Magic:tm: that never really 'clicked' in my head. I can read about the request lifecycle and spend hours in the docs, but what does it _look like_ from a code perspective? How did we get there? Why did they make those choices? Django is an older codebase, so some decisions are assuredly borne of older Python versions and technical limitations over the years; what's _actually required_ to make this stuff work?

Well... Python has a [simple HTTP webserver built in][simpleserver], so could I just subclass that and start expanding on it?

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

...and more! I had a vague idea of what I was looking for, and it mostly boiled down to:

- learning how this worked
- every 


 but there was a specific thing that I wanted to make sure I had: [gunicorn support][gunicorn]. Gunicorn is the standard runner for production software for pretty much every project I've ever worked on ([shoutouts to uWSGI though][uwsgi]), so ensuring that my baby framework could interact with it was paramount. 

## Who needs WSGI anyway?

Gunicorn uses a system called [WSGI][wsgi] (Web Server Gateway Interface) to communicate, so I launched into getting my little framework to speak it. And after poking at it for a while, I had a horrifying realization: there is no way to directly translate `SimpleHTTPServer` to WSGI.

When I started this whole adventure, I thought "you know, the WSGI standard has been around forever, so it's probably not an issue. How hard can this be?" The WSGI standard has indeed been around [since 2003][pep-0333] — which in computing years is essentially forever — but what I'd failed to take into account is that `SimpleHTTPServer` has been around _foreverer_.

{{< image src="/images/basehttpserver_first_commit.png" alt="A screenshot of the first ever commit for BaseHTTPServer, showing August 3rd, 1995 by Guido Van Rossum" caption="For those keeping track at home, this is part of Python 1.3." >}}

## Spiderweb

Clearly, a rebuild was in order. Starting from a [minimal viable example][minimal_wsgi_example] of what serving a WSGI application looks like, I reworked all of my logic to fit into this new paradigm, then began to extend.

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

<!-- footnotes -->

[^example2]:
    This is a footnote.