---
title: "USB-C for Fun and... Nah, Just Fun"
date: 2023-03-03T21:53:31-05:00
summary: "The New 3DS has one problem: a proprietary charging cable. Let's stuff a USB-C port into it instead!"
categories:
  - projects
tags:
  - usb-c
  - repair
  - n3ds
  - nintendo
---

{{< lead >}}
Sometimes the past just needs a little kick to get into the future.
{{< /lead >}}

As I get older, something that annoys me frequently is having to find different cables to charge things. As a direct result of this, I've started tailoring my shopping to find things that I can power with a single connector: [USB-C](https://en.wikipedia.org/wiki/USB-C). This list includes:

* laptop(s)
* both our phones
* monitors
* thumb drives
* xbox controllers
* [my soldering iron](https://pine64.com/product/pinecil-smart-mini-portable-soldering-iron/)
* arc lighter for candles
* ...and other various things

Occasionally, with enough time and research, sometimes I get a craving to dive into my box of parts and forcibly shove a USB-C port into something so that I can eliminate another custom cable from my life. (And yes, I know that sometimes a proprietary cable really is the right way to go for various reasons -- for example, smart watches that don't support wireless charging.)

Today's USB-C adventure involves my new-to-me New 3DS XL. But first:

{{< alert circle-info >}}
For those of you just as confused about the naming as I was, here's the rough layout of the Nintendo DS line:

* Nintendo DS
* Nintendo DS Lite
* Nintendo DSi
* Nintendo DSi XL
* Nintendo 3DS
* Nintendo 3DS XL
* Nintendo 2DS
* New Nintendo 3DS
* New Nintendo 3DS XL <-- you are here
* New Nintendo 2DS XL
{{< /alert >}}

## Why?

I've always been a fan of handheld game systems, and today's handheld game platforms (that are not phones) have a very big problem: namely, the Switch is too big to comfortably fit in your pocket.

My first hand-held console was a teal Gameboy Color in 1996. I loved it to pieces, and some of my favorite gaming memories were spent on the Gameboy Advance and the Gameboy Advance SP. In the years since, I've since refurbished my original Gameboy Advance SP in a fantastic neon green clear shell with a new screen and other upgraded components so that it can live a life of gaming with my brother, but his still relies on the original cable. 

![A neon green Nintendo Gameboy Advance SP.](images/isaacs_gameboy.jpg "I put a lot of hours on this thing back in the day." )

But hey, this isn't about the SP, this is about the 3DS. So let's talk about USB-C.

![A purple Nintendo Gameboy Advance SP charging with a USB-C cable plugged into the back.](images/gb_usbc.jpg "Okay, one glamour shot of my personal SP. Hey, that's a familiar-looking cable...")

## No, not that. Why the 3DS?

That's an even easier question to answer. As far as handheld games are concerned, I've always preferred Nintendo's offerings, and the 3DS (especially the New 3DS) finds itself at a very interesting crossroads. Not only can it play relatively recent games and play them well, it has surprisingly-capable emulation capabilities. From [MAME cabinets](https://en.wikipedia.org/wiki/MAME) to the [Playstation](https://en.wikipedia.org/wiki/PlayStation_(console)) and more, basically everything that I _want_ to emulate (that isn't the glory of the N64 :sob:) is available and working flawlessly.

Plus, the 3DS is officially dead as a platform, which has two primary benefits: [they're _incredibly_ easy to jailbreak](https://3ds.hacks.guide/) and [alternative eShop options](https://hshop.erista.me/) allow... _finding_... whatever game you're interested in for the platform, which is extremely helpful when the official eShop shuts down [later this month](https://en-americas-support.nintendo.com/app/answers/detail/a_id/57847/~/wii-u-%26-nintendo-3ds-eshop-discontinuation-q%26a). The New 3DS XL was manufactured until 2019, so there are still a lot of them floating around, and the sheer number of units with the relatively recent closure of the line means there's a lot of activity in the homebrew and jailbreaking scene.

## So... USB-C.

Mmhmm. USB Type C. It's pretty great if I do say so myself. It is, of course, not without flaws (mostly involving labeling and different cable types), but is otherwise basically my favorite cable. Strategically placed USB-C cables dot my house, enabling charging capabilities beyond my wildest dreams. (There are a couple of Micro-USB cables too; I'm not a monster. But honestly if I could get everything in USB-C, I would.) Every 'special' cable that I can eliminate from my life is one less cable that I have to manage and find a place for.

That's not to say I'm completely against the use of adapters, either; they have their place. If the special cable I'm working with can use 5v in to charge, sometimes it's quite easy to just lop off the end and solder in a USB-C connector with the appopriate resistors so that it can now act as an adapter of sorts on the chargers we already have access to. But sometimes... sometimes it's more fun to just fix the connector.

If the connector you're using is small enough, you might be able to simply unsolder the micro USB port (or whatever was there before) and solder in a USB-C breakout board and map the outputs to the appropriate places on the board. However, this has three potential issues:

* there might not be enough space anyway
* the smaller the connector, the less likely it has the required two resistors in order to set the charge voltage
* any time you have to make substantial changes to an existing circuit board, even more standard additions like this that don't require SMD soldering work, it gets _messy_.

![A picture of a busy workspace with a Gameboy Advance SP motherboard in the center of the table.](images/gb_building.jpg "The number of tools required and the amount of space it takes up is surprisingly large, even though you don't need a lot of specialty equipment.")

You've probably noticed that's a picture of the Gameboy Advance SP again; since I mostly did the 3DS build for me, I didn't really take pictures. But here's one:

![A picture of the back of a New 3DS XL with a suspicious USB-C port added.](images/3ds_usbc.jpg "It took a lot of very careful filing to get to this point. Channel your inner Clickspring.")

## Modding the Console

My original research to the tune of "hey, is this possible" was kicked off by stumbling over [this Reddit post](https://www.reddit.com/r/3dshacks/comments/bvc7d6/i_modded_my_n3ds_xl_to_add_a_usb_typec_charging/) that shows some basic information on actually performing the mod, though definitely not a full walkthrough. It's useful to get the location of where to solder to the motherboard, but the rest isn't very useful.

We both used [this USB-C breakout board](https://www.sparkfun.com/products/15100) from Sparkfun; at $5 a piece, they aren't the cheapest but they already have the resistors in place to request a 5v supply from the other end of a USB-C <-> USB-C cable, which is critical for this application and also means I don't need to deal with surface-mount components (which makes me a happy camper).

In their design, they trimmed away a somewhat substantial portion of the support material around the tip of the stylus in order to fit the board into place; the trick here is that it's very close to the shoulder buttons and the ZR button has a bit of internal travel inside the case. The board itself has quite a lot of extra space on it even for how small it is, so I opted for a slightly more violent method: reshaping the PCB itself instead of trimming away as much of the case. By removing a lot of the extra unused PCB, it fit nicely in a space closer to the button and gives the back of the console a much cleaner look in my opinion. The important parts are removing both of the sections of PCB for the mounting holes, as with careful installation it butts perfectly against the internal shape of the battery housing. In fact, in my console, the port is not held in place by anything but the pressure of the case and weaseling it into the single spot that it fits.

I'll be honest; this install was a _bear_. The motherboard has eight micro ribbon cables on three of the four sides, and two of those ribbon cables are on the bottom of the motherboard. Of the eight cables, they use _three_ different connection methods; I guess because screw you, that's why? [This video on performing a motherboard swap](https://www.youtube.com/watch?v=x2pr1j6DJ3E) was instrumental for learning how to remove each one in a way that doesn't damage all the connectors.

I'd show you the inside of mine, but I'm hesitant to open it again. As it stands, you'll have to take this as proof that it works:

![An image of a charging 3DS with a USB-C cable attached to the back.](images/3ds_showing_charging.jpg "Charge, baby, charge.")

Would I do this again? No, I don't think so. The entire install took about 3.5 hours for me, and they weren't particularly fun. However, I'm super stoked about the newfound functionality of the console and am looking forward to putting it to the test during some travel later this year.

Here's to our favorite games of today and yesterday! :clinking_glasses:

## Additional Resources

* https://consolemods.org/wiki/3DS:New_3DS_XL_USB-C_Charging_Port_Mod
