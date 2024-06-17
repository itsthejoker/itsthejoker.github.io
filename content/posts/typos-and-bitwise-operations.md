---
title: "Typos and Bitwise Operations"
date: 2024-06-17T11:29:40-04:00
draft: true
summary: "Sometimes typos turn out to be unary operators in disguise."
categories:
  - python
tags:
  - python
  - terminal
---

## Sometimes Typos Can Be Fun

A little bit ago, I was playing around with some code in the Python REPL[^repl] and made a typo that spawned a whole rabbit hole of reading. 

```python title="Python REPL"
>>> x = 4
>>> x
4
>>> ~x  # Typo! Where'd that ~ come from?
-5
```

{{< image src="/gifs/keanu-reeves-head-tilt-confused.webp" alt="Keanu Reeves tilting his head with a 'wtf' expression." caption="Definitely me staring at my screen." >}}

Time to do some digging.

## Evil bitwise hacking

Let's start with a quick explanation of what we're actually looking at here, because some of the terms are confusingly similar.

{{< admonition type=info title="Definitions!" >}}
**Bit**: A one or a zero. Multiple bits come together to form a byte, which can communicate information.

**Byte (Octet)**: A byte is eight bits. For example, the letter "a" (specifically the lowercase version) is one byte in size and looks like this: `01100001`.

**Nibble**: Only four bits — half of a byte and capable of representing numbers from 0 to 15. For ease of reading, we'll be mostly using nibbles as examples throughout this post.

**Binary Numbers**: how computers view numbers. This can be a very deep topic, but the gist of it is that all integer numbers are made of bytes. A nibble (a four-byte number) is something like 0000 or 1010, and the way that you read it is by starting at the right and counting left in powers of two. If we look at 1010, you read it by breaking it apart into places. Since there are four places, the meanings of each place are **8-4-2-1**. Taking this, we can use our binary number (`1010`) and look at the values to figure out what we have: `(1 * 8) + (0 * 4) + (1 * 2) + (0 * 1)`, or 8 + 2 = 10. By the same logic, `0000` is `(0 * 8) + (0 * 4) + (0 * 2) + (0 * 1)`, which turns out to be a big whopping zero.

**Binary Arithmetic**: Any operation or modification that involves two numbers, like multiplication or addition.

**Unary Arithmetic**: Any operation or modification that only involves one number.

**MSB**: Most Significant Bit. It's the one on the farthest left.
{{< /admonition >}}

Note that this is all kind of a pain and rather more complicated than it seems to need to be, but a certain amount of complexity is what allows computers to do a lot of math _very_ quickly, and doing it quickly is really what's important here.

Going back to the original question of "what in the world happened when we ran `~4`", it turns out that `~` is a `unary operator`, in that it does math on a single number. Specifically, what it does is it performs a "NOT" operation on the number. A NOT operation flips all of the bits from 0 to 1 (or vice versa). This is what that looks like (spoiler alert: I'm about to ruin this and make it more complicated):

```
100  # Starting with 4...
↓↓↓  # ...invert the bits.
011  # This looks like 3, but it's not. I'll explain why.
```

This interaction [is called a "Two's Complement"][twoscomplement], and is used by pretty much all modern computers. (As opposed to the [One's Complement][onescomplement], which you can read about separately if you're interested.) I deliberately left some pieces off of the earlier example, so let's look at it again. The first thing we need to do is tack on another bit to the left side, and we'll use that to keep track of whether a number is positive or negative. 0 is positive, 1 is negative.

```
0 100  # positive 4
↓ ↓↓↓  # invert the bits
1 011  # negative... five?
```

Here's where it gets _real weird_. When reading the complement (the inverted version), you treat the Most Significant Bit (MSB) as a number... that you subtract the others from. The way you read the last number is:

```
1 0 1 1  # MSB = 1, so it's negative
8 4 2 1  # just to remember the places that everything means
-------
8 0 2 1  # Normally, we'd sum these together.
         # However, there are two things different
         # here: one is that the MSB is 1, which means
         # it's negative, so we actually have:
-8 0 2 1
         # Second, we want to take the MSB and
         # subtract the others from it, which looks
         # like this:
-8 - (2 + 1)
-8 - 3
------
-5       # ...and there's our result. NOT 4 is -5.
```

Fun fact: to get the proper negative version of your starting number, it's the same process as outlined above, just with adding 1 (0 001) to the number before 'assembling' it with the MSB. 

## What can you do with it?

## Wrapping up


<!-- links -->

[onescomplement]: https://en.wikipedia.org/wiki/Ones%27_complement
[twoscomplement]: https://en.wikipedia.org/wiki/Two%27s_complement

<!-- footnotes -->

[^repl]:
    The Python read-eval-print-loop system that runs when you just type `python` in your terminal.
