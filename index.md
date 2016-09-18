---
layout: page
title: Joe Kaufeld
tagline: Supporting tagline
---

# Welcome!

Thanks for stopping by; I post weird stuff, work stuff, and stuff that I learn
in my projects. Feel free to shoot me an email if you have any questions --
otherwise, stick around and maybe we'll learn something together!


# Latest Post:
<li>
{% for post in site.posts offset:0 limit:1 %}
  <a href="{{ post.url }}">
  <h3>{{ post.title }}</h3>
  {{ post.content |truncatehtml | truncatewords: 30 }}
  {% endfor %}
<p>
