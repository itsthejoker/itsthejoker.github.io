---
layout: post
title: "What is good logging in Python?"
description: "A slightly-more-indepth look at Python's logging capabilities"
category: python
tags: [python, tips, logging]
---
{% include JB/setup %}

(A/N: This post was originally written for and published by <a href="https://smartfile.com">SmartFile</a>)

When writing a script or trying to debug a larger program, logging is your
friend. Have you ever found yourself adding lots of print statements to try
and find the information you need? By properly setting up Python’s logging
module, you can save yourself some major headaches!

When I first started writing scripts, I wrote my own logging “system” in every
program. It usually ended up looking something like this:

{% highlight python %}
def log_info(message):
    print("INFO - {}".format(message))

def log_error(message):
    print("ERROR - {}".format(message))
{% endhighlight %}

This is definitely useful, but even for quick debugging it’s pretty iffy. If we invoke Python’s built-in logging module, we can reproduce this behavior in about the same number of lines:

{% highlight python %}
import logging

logging.info("This is an info message!")
logging.warning("This is a warning message!")
{% endhighlight %}

Logging has five levels of severity: debug, info, warning, error and critical.
By default, Python’s logging module only prints warning,error and critical
messages, so only the second message would print to the console in the above
example.

If you keep it at the default configuration, it looks like this:

{% highlight bash %}
WARNING:root:This is a warning message!
{% endhighlight %}

By itself, that’s not tremendously pretty, nor does it give us more information than we started with. Let’s see what happens if we configure the logger ourselves:

{% highlight python %}
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - [%(levelname)s] - %(message)s')

logging.info("This is an info message!")
{% endhighlight %}

Important note: when sending a message to the logger, you use the lowercase
version (logger.info(“this is my message!”)). When setting a level
(logger.setLevel(logging.INFO)), you need the uppercase version. This is a
common “gotcha” for people new to the logging library!

Now we get a lot more information, just by that one change:

{% highlight bash %}
[2016-08-09 11:21:02,326] - [INFO] - This is an info message!
{% endhighlight %}

This is definitely good information to have, and as a bonus, it’s clear and easy
to understand! In the above example, the only formatting bits the logger actually
cares about are %(asctime)s, %(levelname)s and %(message)s.

Those aren’t the only ones, though; what happens if we put %(funcName)s into our
logger?

{% highlight python %}
FORMAT = '[%(levelname)s] - [%(funcName)s] - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

def test_function():
    logging.debug("This is a debug message!")

def second_function():
    logging.warning("This is a warning message!")

test_function()
second_function()
{% endhighlight %}

I’ll give you a hint; it looks like this!

{% highlight bash %}
[DEBUG] - [test_module] - This is a debug message!
[WARNING] - [second_module] - This is a warning message!
{% endhighlight %}

If you’re working with scripts that are all in one file, having logging of this
type is incredibly useful. But what if you’re working with something even larger?

The root logger is fairly limited; it can only log one thing with one format.
For example, that means you can’t write the log to a file and to the console at
the same time. Fortunately, there’s a graceful way to overcome that in the form
of “handlers.” Let’s look at adding a handler so we can log to file only, then
having both the console and log file report the same thing:

{% highlight python %}
import logging

# create the logging instance for logging to file only
logger = logging.getLogger('Test')

# create the handler for the main logger
file_logger = logging.FileHandler('test.log')
NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
logger.addHandler(file_logger)

# remember that by default, logging will start at 'warning' unless
# we set it manually
logger.setLevel(logging.DEBUG)

# log some stuff!
logger.debug("This is a debug message!")
logger.info("This is an info message!")
logger.warning("This is a warning message!")
{% endhighlight %}

The above will create a file in the same directory as the script with the same
type of output as before. What if we want to log the same thing to the file and
the console? If we add the following lines after logger.setLevel(logging.DEBUG)…

{% highlight python %}
# now we can add the console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('Test').addHandler(console)
{% endhighlight %}

…then we get the same output in the file, but now we get the following on the console:

{% highlight bash %}
This is an info message!
This is a warning message!
{% endhighlight %}

Notice that the formatting didn’t carry over; we have to declare our own
formatting for the new handler. In this case, we’ll just use the “NEW_FORMAT”
variable that we declared earlier.

{% highlight python %}
# now we can add the console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# declare the new format
console_format = logging.Formatter(NEW_FORMAT)
# tell the handler to use the new format
console.setFormatter(console_format)
logging.getLogger('Test').addHandler(console)
{% endhighlight %}

Now we get the same formatting (date, time, level and message) in both the console and the file!

There’s a lot more you can do with Python’s logging module, but I’d like to
leave you with my favorite optimization tweak for logging. When creating a
bunch of statements in one block, you can perform one check for all of them
to see if they should be printed.

{% highlight python %}
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("things")
    logger.debug("more things")
    logger.debug("EVEN MORE THINGS")
{% endhighlight %}

Proper logging is absolutely necessary in any decently sized application; even
small apps benefit from knowing exactly what variable is getting passed where or
finding out what’s broken. At SmartFile, we log everything our applications do
and utilize many of the features of Python’s logging module — there’s no job too
big or too small!

If you’re interested in learning more about Python’s logging library, here are
some good resources:

* <a href="https://docs.python.org/3/howto/logging.html">
  Python 3’s logging docs</a>
* <a href="https://docs.python.org/2/howto/logging.html">
  Python 2’s logging docs</a>
* <a href="https://docs.python.org/3/howto/logging-cookbook.html">
  Python 3 Logging Cookbook</a>
* <a href="http://victorlin-blog.logdown.com/posts/2012/08/26/good-logging-practice-in-python">
  Excellent writeup from Victor Lin about advanced usage of Python logging</a>
