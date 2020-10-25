Title: Intro to Distributed Computing with Python over a LAN
Date: 2016-09-17 10:20
Modified: 2016-12-05 19:30
Category: python
Tags: python, cluster, supercomputer, instructions
Slug: intro-to-distributed-python
Summary: Setting up ParallelPython on any OS to make your own cluster!

(A/N: This post was originally written for and published by [SmartFile](https://smartfile.com)

To some, a personal supercomputer or cluster for home or business is planted firmly in the realm of *Those Who Have Too Much Money*. For others who know better, there’s the [**Beowulf Cluster**](https://en.wikipedia.org/wiki/Beowulf_cluster).

Essentially, a Beowulf Cluster is a set of normal consumer machines networked
together to crunch data as a single entity. In this article, we’re going to cover using distributed computing with Python over a LAN to create a Beowulf Cluster so you can improve computing power and efficiency without breaking the bank.

We’ll be taking a look at making your own Beowulf Cluster using equipment you probably already have and some open-source software. The individual pieces are listed below. Without further ado, let’s begin our intro to distributed computing with Python over a LAN!


### Hardware for the Beowulf Cluster

* 2+ computers (OS independent! Windows, OSX, and Linux are all welcome)
* 1 switch/router/combo unit – the abilities we’re looking for are:
  * Can the computers get an IP address?
  * Can the computers successfully communicate?

### Python Software & Libraries

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [Parallel Python by Vitalii Vanovschi](http://www.parallelpython.com/)

We’ll be using Parallel Python because a) it allows us to create and remove nodes at will simply by running a Python script and b) everything communicates over HTTP using auto-discovery, which means we don’t have to worry about specialized networks or setting up a parallel processing system like [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface). (It also lets us end with a pure Python implementation!)

# Setting Up the Cluster Environment

Let’s start by getting our environment set up; for purposes of this tutorial, we’re making the following assumptions:

* You know what Python is
* You know how to get it working on the command line for whichever OS you have
* You have an idea that can take advantage of the vast capabilities of distributed processing

All that being said, we’ll be using [virtualenv](https://virtualenv.pypa.io/en/latest/) to get our environment set up, but if you either don’t want to use virtualenv or just work on things that only you’ll use, you can skip the virtualenv-specific stuff. If you’ve never heard of virtualenv, take a look [**here**](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to get some more information.

# Getting Started on the Cluster

We’ll start by using virtualenv to create our working directory:

    :::bash
    virtualenv cluster
    cd cluster
    source bin/activate

After running the three commands, we should see something that looks like this (disclaimer: I’m on Linux, so if you’re using Windows you’ll see something slightly different):

    :::bash
    (cluster) [jkaufeld@localhost cluster]$

To close down your new environment, just run `deactivate` and it will return you to the normal command line.

Here we install the processing library, Parallel Python.

    :::bash
    pip install pp

We’ll test it by running python in the terminal and typing in `import pp`. If we don’t get an error, it installed correctly!

# Getting into Parallel Python

Parallel Python (or PP as I’ll be writing it as from now on) has a fairly simple structure that makes it easy to quickly draft out programs. The basic structure looks like this:

    :::bash
    [imports]
    [function(s) to be sent to the nodes]
    [server logic]
    [retrieve results from nodes]


While the examples on the website are fairly comprehensive, the actual documentation is somewhat dense at times. Here, we’ll make a quick script that we can use to identify nodes on our network as we add them. To start with, it will only return information on the host computer (since we haven’t added any nodes yet!).

    :::python
    import pp

    ppservers = ("*",)  # autodiscovery mode on!

    # create the job server
    job_server = pp.Server(ppservers=ppservers)

    print "Starting pp! Local machine has {} workers (cores) available.".format(job_server.get_ncpus())

That’s all there is to it. Run the above and you should see the number of processor cores present on your local machine. (Note that the above script does not have the “[function(s) to be sent to the nodes]” part; we’ll add that later!) Congratulations, we have a functioning parallel computational system! Now, it’s not much to write home about, so let’s add a node or two.

#### Important notes here:

* It doesn’t matter what OS we use
* Make sure that the default port of 60000 is open in the firewalls of your host machine and your node(s)
* It’s easier here to simply download the .zip from the Parallel Python website, as we’ll only need access to one specific file inside PP

# Adding Additional Nodes

In my testing environment here, I have a Windows machine that I’ll set up as a node. After downloading and extracting the parallel python .zip to my downloads folder, all I need to do (after verifying the port is open in the firewall!) is run:

    :::bash
    C:\Users\Tester\Downloads\pp-1.6.5> python ppserver.py -a

We need to run ppserver.py with the `-a` flag so that it starts in autodiscovery mode; if we need to verify that it’s actually working, we can also tack on the `-d` flag to toggle debug mode. Now that the script is running, we have a running node – let’s head back to our primary machine.

All we should have to do to reflect this new change to the environment is add two extra lines to the bottom of our current script:

    :::python
    for computer, cpu_count in job_server.get_active_nodes().iteritems():
        print "Found {} with CPU count {}!".format(computer, cpu_count)

It should return something like this:

    :::bash
    Found 192.168.1.149:60000 with CPU count 2!
    Found local with CPU count 4!

# Doing Evil with Distributed Computing

Not bad! Now we can actually have some fun. As an example of some things this software can really do, we’ll simplify the first example from the website.

    :::python
    #!/usr/bin/python
    # File: sum_primes.py
    # Original author: Vitalii Vanovschi
    # Desc: This program demonstrates parallel computations with pp module
    # It calculates the sum of prime numbers below a given integer in parallel
    # Parallel Python Software: http://www.parallelpython.com

    import math
    import time
    import pp


    def isprime(n):
        """Returns True if n is prime and False otherwise"""
        if n < 2:
            return False
        if n == 2:
            return True
        # no reason to go through all the numbers; the square root is as far as
        # we'll get anyway
        max = int(math.ceil(math.sqrt(n)))
        i = 2
        while i <= max:
            if n % i == 0:
                return False
            i += 1
        return True


    def sum_primes(n):
        """Calculates sum of all primes below given integer n"""
        return sum([x for x in xrange(2, n) if isprime(x)])

    # tuple of all parallel python servers to connect with, or "*", for
    # autodiscovery
    ppservers = ("*",)  # the comma is important!

    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

    print "Starting pp with", job_server.get_ncpus(), "workers"

    start_time = time.time()

    # The following submits 8 jobs and then retrieves the results
    inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
    jobs = [(input, job_server.submit(sum_primes, (input,), (isprime,), ("math",))) for input in inputs]
    for input, job in jobs:
        print "Sum of primes below", input, "is", job()

    print "Time elapsed: ", time.time() - start_time, "s"
    job_server.print_stats()

It follows the same basic structure that we laid out above, with the only added addition of having two functions that need to be passed to the nodes. The important line that’s new from the last example is this:

    :::python
    job_server.submit(sum_primes, (input,), (isprime,), ("math",))


This is the core, the part where all the magic happens. The order looks like this:

    :::python
    job_server.submit(
        primary_function,
        (tuple, of, input),
        (tuple, of, assisting, functions),
        ("tuple", "of", "required", "modules")
    )

Note that even if you’ve only got one thing to pass to the job server, it still needs to be a tuple – those commas will bite you if you don’t watch out.

There are several different ways to get information out of the job server; one way is to use a generator as shown above. Another looks like this:

    :::python
    jobs = []

    jobs.append(job_server.submit(sum_primes, (input,), (isprime,), ("math",)))

    # gather results
    for job in jobs:
        result = job()
        if result:
            break

    if result:
        print result
    else:
        print "Sorry, couldn't find anything."

# Concluding Thoughts

No matter what you’re looking to use Python parallel processing for, the means are definitely within your grasp. While distributed computing with python is not as fast as other methods, it’s by far the easiest to set up and get going. I’ve personally run this on all sorts of operating systems and all sorts of hardware – everything from servers to Raspberry Pis can handle this kind of computation without breaking a (digital) sweat. With hardware becoming cheaper by the day, a personal Beowulf Cluster isn’t science fiction anymore; in the words of someone smarter than me, “go thou and learn”!
