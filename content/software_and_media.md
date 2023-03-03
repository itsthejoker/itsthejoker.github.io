---
title: "Software & Media"
date: 2023-02-28T21:20:33-05:00
showDate: false
showAuthor: false
showWordCount: false
showReadingTime: false
---

{{< lead >}}
My favorite projects and places you can see or hear me!
{{< /lead >}}

## Open Source Software

### FilamentColors.xyz

[{{< icon github >}}](https://github.com/itsthejoker/filamentcolors.xyz) [{{< icon internet-access >}}](https://filamentcolors.xyz)

In 3D printing, getting the right color of filament for a project is often a pain. Have you ever wondered "what filament do I need to get to match this color?" or "what looks good with this filament I already have?" These are questions FilamentColors.xyz tries to answer by providing a filament color database with over a thousand different filaments from all over the world -- each one printed, measured, and automatically grouped into pre-built color palettes ready for you to use in your next project!

### Grafeas Group, Ltd

[{{< icon internet-access >}}](https://grafeas.org)

A small international nonprofit that I co-founded with James Coe, this registered 501(c)3 in the US has over 5,875 volunteers and aims to increase accessibility on the internet. By creating text versions of internet content, everyone has a chance to participate in the discussion. Our volunteers have, at the time of this writing, completed over 270,000 transcriptions and descriptions online and through Reddit for those who need them.

The organization uses six bots total; three on Reddit's side and three internal bots for managing ourselves and our community.

### Grafeas: The External Bots

#### u/transcribersofreddit

[{{< icon github >}}](https://github.com/grafeasgroup/tor) [{{< icon reddit >}}](https://reddit.com/u/transcribersofreddit)

The primary bot that volunteers interact with, this bot is responsible for finding new content, posting it to the subreddit, and working with volunteers as they complete transcription jobs. This is the first bot that I wrote for the project, and the very first version was knocked out in my airb&b room in between PyCon sessions in 2017!

#### u/transcribot

[{{< icon github >}}](https://github.com/grafeasgroup/tor_ocr) [{{< icon reddit >}}](https://reddit.com/u/transcribot)

Sometimes it's helpful to have a starting point for some of the longer transcriptions, so u/transcribot runs each and every picture through OCR and posts the (often hilariously wrong) results where the volunteers can access them. It follows u/transcribersofreddit around our subreddit, toddling along and trying its best.

#### u/ToR_Archivist

[{{< icon github >}}](https://github.com/grafeasgroup/tor_archivist) [{{< icon reddit >}}](https://reddit.com/u/tor_archivist)

Arguably the least-known of the trio, the Archivist takes completed posts, grabs the link to the actual completed transcription, and posts it to [the TranscribersOfReddit Archive](https://reddit.com/r/ToR_Archive) for folks who need it. It also removes posts from the primary job board as they 'age out' if no one claims them.

### Grafeas: The Internal Bots

#### Blossom

[{{< icon github >}}](https://github.com/grafeasgroup/blossom)

The Django monolith that powers it all and the keeper of our data! Blossom is where all of our central processing takes place; the other five bots make very few decisions for themselves and mostly look to Blossom for guidance. Blossom also powers [the organization homepage, grafeas.org!](https://grafeas.org)

#### Bubbles

[{{< icon github >}}](https://github.com/grafeasgroup/bubbles)

Every organization needs an overly chatty chatbot, and Grafeas is no different. Bubbles runs in our internal Slack and assists with anything we need -- anything from gathering data on potential subreddits to providing pictures of cute animals to handling our deployments of all six bots (including herself!) to production!

#### Buttercup

[{{< icon github >}}](https://github.com/grafeasgroup/buttercup)

Buttercup runs our volunteer Discord! Host to a whole bunch of cool commands and data visualization stuff, Buttercup helps enforce username standards and also allows volunteers to track their progress on various challenges and get access to other cool data to see how they're doing.

### Grafeas: The Other Stuff

Occasionally we work on other systems as we prototype ideas or spin out functionality into other repositories as needed.

#### Utonium

[{{< icon github >}}](https://github.com/grafeasgroup/utonium)

As we grew Bubbles, we realized quickly that the `slack-bolt` package that Bubbles used was not really designed to handle all the commands that Bubbles has, so I designed a plugin system from the ground up to handle the (vaguely ridiculous) number of Slack commands that we need to handle across different platforms. It's not the easiest to integrate, but works well for our needs!

#### Caroline

[{{< icon github >}}](https://github.com/grafeasgroup/caroline)

An idea that we toyed around with for using Redis or Elasticsearch as a pseudo-relational backend that relies on JSON Schema for validation. Still a project that I'm quite proud of, even though I'm not sure it should ever actually be used.

### asbestos

[{{< icon github >}}](https://github.com/spotoninc/asbestos)

At SpotOn, we work with a lot of data in [Snowflake](https://www.snowflake.com) but there ~~is~~ was no way to mock the connection cleanly for testing functions that use Snowflake data or for developing against a Snowflake call and paying to run the same query over and over. Enter `asbestos`, a project named after the fake snow from _The Wizard of Oz_. (That's true: the snow used in the movie is 100% pure asbestos. Horrifying, isn't it?) Asbestos allows you to mock the Snowflake connection, store SQL queries and expected answers, and then spit back the answers when you call Snowflake normally.

Fun fact: the original name for this project was `snowfake`, but Snowflake's lawyers told us we couldn't do that. :sob:

### emailmagic

[{{< icon github >}}](https://github.com/itsthejoker/emailmagic)

`mailto:` links are annoying, and it's weird to me that we don't have an industry solution to this problem yet. `emailmagic` watches for `mailto:` links, then makes the link pop up a modal so you can open the link in your preferred email client or just use the default browser behavior. On the sites that I write myself (e.g. not this one), I use [Bootstrap](https://getbootstrap.com/) as my UI library of choice so that I don't have to reimplement everything from scratch, and `emailmagic` is styled using Bootstrap 5 so that it can be a clean drop-in addition. See the readme for more information.

### What day is it?

[{{< icon github >}}](https://github.com/itsthejoker/emailmagic) [{{< icon internet-access >}}](https://itsthejoker.github.io/whatdayisit)

Have you ever wished that you had a very specific yet startlingly useless way of identifying what day it is? Do I have the answer for you...!

### Yarn Calc-inator

[{{< icon github >}}](https://github.com/itsthejoker/yarncalcinator) [{{< icon internet-access >}}](https://itsthejoker.github.io/yarncalcinator)

A basic meters <-> yards conversion tool for identifying how many skeins of yarn you need to purchase for a pattern if the measurements are different or the amount of yarn in each skein is different. Written for my partner to aid in her crochet projects.

## Media

### 2020-04-21 | Makers On Tap Podcast, Episode 76

[{{< icon internet-access >}}](http://www.makersontap.com/e/mot-076-joe-the-filament-librarian/)

Makers On Tap is a podcast by makers, for makers - we chatted about filamentcolors.xyz, accessibility, nonprofits, and general life.

### 2020-04-20 | Faraday Tech Cafe Podcast, Episode 15, Part 2

[{{< icon internet-access >}}](https://faradaytechcafe.podbean.com/e/episode-15-part-2-accessibility-on-the-web-and-in-coding-schools-with-joe-kaufeld/)

Hosted by Gwen Faraday, this is part two of a long-form interview covers some of my history and mostly focuses on Grafeas and TranscribersOfReddit.

### 2020-04-13 | Faraday Tech Cafe Podcast, Episode 15, Part 1

[{{< icon internet-access >}}](https://faradaytechcafe.podbean.com/e/episode-15-internet-accessibility-for-developers-with-joe-kaufeld/)

Hosted by Gwen Faraday, this is part one of a long-form interview covers some of my history and mostly focuses on Grafeas and TranscribersOfReddit.

### 2020-04-05 | VRRF 2020 // Virtual Reprap Festival

[{{< icon youtube >}}](https://www.youtube.com/watch?v=EzypNyAK3Xc&feature=youtu.be&t=1327)

Since the Midwest Reprap Festival (MRRF) was cancelled due to COVID, it happened over YouTube instead! I was able to present and discuss filamentcolors.xyz.

### 2020-02-23 | WIRED

[{{< icon internet-access >}}](https://www.wired.com/story/online-altruists-are-making-reddit-more-accessible/)

This is the same article from WIRED UK, but syndicated to the main site!

### 2020-02-23 | WIRED UK

[{{< icon internet-access >}}](https://www.wired.co.uk/article/transcribers-of-reddit)

Interview from Alex Lee of WIRED UK about Grafeas, TranscribersOfReddit, and the international impact of our work.