# Intro to 3D Printing, Part 1


## What is this 3D printing thing?

There's a lot of information about 3D printing as a hobby, but what does that all boil down to? What do you need to get started? What do you need to know before bringing a printer into your house? What kinds are there?

The goal of this series isn't to be an all-encompassing introduction; mostly, we'll touch on the core concepts and give you terms and ideas that you can research later.

## What is 3D Printing and what is a 3D Printer?

You already know about printing on paper. 3D printing is a lot like that, but the result is a physical thing rather than text on a page. Instead of ink, a 3D printer uses plastic; instead of reproducing the text on a computer screen, a 3D printer reproduces a digital model that you process and download to it.

You can 3D print almost anything. Here are some examples:

* a doorknob
* a leg for that display stand that broke a while ago
* a bowl for your keys
* an adapter that fits on a vacuum
* a figurine
* a piece of art
* a jig to help do something
* a mobility aid to help open jars
* a robot body
* a mount for a piece of technology

...there are so many options that you're mostly limited by the physical properties of plastic and your imagination. With that in mind, let's talk about the second question: what is a 3D printer?

{{< admonition type=info title="" >}}
A machine that takes a physical medium (plastic, metal, concrete, chocolate, etc.) and carefully arranges it in a specific shape when guided by a computer.
{{< /admonition >}}

The most common type is one that melts strands of plastic about the diameter of pencil lead into strips the width of a piece of string. Have you ever had a _ball_ of string? Even though the string itself doesn't take up much space, it builds on itself when you have a lot in one place. That's the same concept that most consumer 3D printers operate on.

{{< admonition type=info title="" >}}
There are a lot of different options with what type of printer to use and what kind of material to use -- like types of fabric, there are hundreds of choices. For this, we'll only focus on the most common options.
{{< /admonition >}}

## What You Need

To get started with 3D printing, you'll need a handful of things:

* a 3D printer
* a computer
* a way to get information from the computer to the printer -- options include:
    * USB cable
    * USB thumbdrive
    * SD card
    * Some printers can even connect to your local network!
* a program called a [slicer](https://en.wikipedia.org/wiki/Slicer_(3D_printing))
* material for the printer to use
* patience


We're going to cover that list out of order because there are some terms that we have to get to first.

### Patience

Although it doesn't seem like it belongs there, you'll notice that `patience` is definitely on that list. 3D printing is a very cool process, but it's not a perfect process. There will be configurations that you have to modify, bolts that will need adjusting, bearings that will need oiling, and results that will need tweaking. This is just a part of the hobby, and if those things do not sound exciting or interesting, then this may not be the hobby for you.

It is worth noting that there are machines that don't require anywhere near as much maintenance / "hand-holding" in order to continue working, but they are usually several thousand dollars (or more). If you're approaching this from the hobbyist standpoint, at least some amount of tinkering will be required.

### The Material That Gets Printed

Material for 3D printing, called `filament`, is a very long connected line that is usually wound onto a spool. These spools are sold by weight in one (1) kilogram (2.2 lbs) rolls. The filament is sold in two diameters:

* 1.75mm diameter
    * Industry standard -- the majority of printers use this size
* 3mm diameter
    * This is older and not used as much anymore

{{< admonition type=tip title="" >}}
Consumer 3D printing is entirely based in the metric system. Besides the fact that the metric system is very easy to use, 3D printing is heavily rooted in [open source](https://en.wikipedia.org/wiki/Open_source); the first open source 3D printer, the [RepRap](https://reprap.org/wiki/RepRap), was created in Bath, UK, in 2004.
{{< /admonition >}}

The most common, beginner-friendly material to print with is known by its acronym: [PLA](https://en.wikipedia.org/wiki/Polylactic_acid). It's not very expensive, is easy to work with, and makes reasonably strong parts. There are many different options -- [PETG](https://en.wikipedia.org/wiki/Polyethylene_terephthalate#Copolymers) and [ABS](https://en.wikipedia.org/wiki/Acrylonitrile_butadiene_styrene) are also popular, but they usually require some modifications / upgrades and special ventilation and temperature control to use properly.

### The Slicer

Though it has an ominous name, a slicer is a program that takes a digital model and converts it into instructions that the 3D printer can interpret. These instructions are very detailed and contain all the information needed for a specific 3D printer to build the model. Sliced files (the sets of instructions) are specific to the printer they're created for; if they're given to a different brand or build of printer, unexpected issues (or potentially damage to the printer) may occur.

Sliced files are known as `gcode` files; gcode is the instruction set that almost all 3D printers use. It's [also used](https://en.wikipedia.org/wiki/Numerical_control) by some larger manufacturing tools, like automated [mills](https://en.wikipedia.org/wiki/Milling_(machining)) and [lathes](https://en.wikipedia.org/wiki/Lathe). You can [read more about gcode here](https://en.wikipedia.org/wiki/G-code) if you're interested.

### The Computer

As long you have a computer or laptop (not a tablet or smartphone) that runs Windows, Mac OS X, or Linux, then you can find a slicer to use. The three most popular free slicers ([PrusaSlicer](https://www.prusa3d.com/prusaslicer/), [Slic3r](https://slic3r.org/), and [Cura](https://ultimaker.com/software/ultimaker-cura)) run on all three operating systems and are very forgiving on slower computers.

### A 3D Printer

The printer itself is where the magic happens -- where everything finally combines to produce a 3D printed object. It takes the sliced file (the gcode file) and the filament, then uses the gcode instructions to build the object one move at a time.

To achieve this, the 3D printer uses specialized heaters to melt the filament to very small widths and carefully deposit it onto a build plate (usually glass or another material) so that it can build upwards by putting down more layers of plastic down. Layer by layer, very slowly, an object is built up from the build plate. This process usually takes a long time; even small objects can take much longer than expected. Most small prints can be accomplished in 30 minutes to an hour; it's not uncommon for prints to take two, four, or even 24 hours to complete depending on the size and level of detail.

## Wrapping Up

In this post, we've covered some core concepts of 3D printing; what 3D printing actually looks like and what it entails. Next week, we'll go over the next steps: the stuff you need to know and what you need to do before buying a 3D printer.

