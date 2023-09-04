# Joplin and Fastmail


## Sometimes de-Googling leads to interesting solutions

As I continue my quest to slowly cut more and more Google services out of my world, I knew that eventually I would need to break my dependence on Google Docs and Google Keep as a way to keep track of thoughts and writing. Eventually I found, with the help of some friends, a solution that works really well for me and I'd like to share it with you!

## The Requirements

When looking at what Google Docs and Keep brought for me, it was fairly easy to separate the things I cared about from the things I didn't care about.

### Things I cared about

* Access via mobile and desktop
* Edit abilities on mobile and desktop, not just read
* Create abilities on mobile and desktop
* Text formatting
* Easily create new notes for reference later
* Reference notes need to be quickly searchable
* Should be able to do long-form writing as easily as short-form writing
* Willing to pay a little, but should be pretty cheap
* Preferably uses Markdown for text formatting

### Things I did not care about

* Very fancy editing interface
* Powerpoint-esque features
* Excel-esque features
* Web interface

Since I'm primarily using text here, I started by looking for applications that have a mobile app and can run on desktop as well. I started with [Obsidian][obsidian], but did not end up sticking with it as I felt that it focused more on looks over functionality. Obsidian also pushes the "mind mapping" technique of data organization, which doesn't really do a lot for me.

Eventually, I found [Joplin][joplin], which is not quite as polished as Obsidian, but did accept markdown editing and was quite extensible (and easy to write extensions for!). Their documentation was great, there's a mobile app, and I was off to the races.

## How to handle syncing

Now, the question is how to handle syncing the notes across mobile and desktop. Joplin offers the [Joplin Cloud][joplincloud], a paid (or self-hosted!) service for syncing. It is fast and works well, but one of my friends had a suggestion; Joplin supports many different methods of syncing, and one of the "you kind of have to dig for it in the settings" options is to use [WebDAV][webdav]. It's a bit on the old side and isn't tremendously fast, but it's an option. And with that option, enter [Fastmail][fastmail]. ([Click here][fastmail_referral] for 10% off your first year!)

Fastmail has been my go-to mail provider for a while, and a feature I didn't realize they offered is actually a functional [WebDAV Files section][fastmail_webdav] that you have full control over. Ideally they probably intend for you to use this as more of an emergency file storage (if you use it at all), but it also turns out it works quite well in Joplin!

## Setting up Fastmail WebDAV in Joplin

If you want to give this a try, setting it up is fairly straightfoward.

In Fastmail, visit the `Integrations` page [by clicking here](https://app.fastmail.com/settings/security/integrations), then "New App Password". On this screen, you can set a name for your new integration and the things it's allowed to access; WebDAV is the only thing you need here.

![Screenshot showing the Fastmail 'create new integration' screen.](images/fastmail_new_app_password.png "Looks like this!")

After clicking `Generate password`, you'll get a randomly generated password that is specific to that integration. Save it now because you won't be able to see it again.

In Joplin, go to Settings -> Synchronization. You'll only need a few things to make this work:

* Set Synchronization target to WebDAV
* WebDAV URL: https://myfiles.fastmail.com/Joplin
* WebDAV Username: your fastmail email address
* WebDAV Password: the randomly generated one that Fastmail gave you

Click on "Check synchronization configuration" below, and you should see the following message:

![Screenshot of Joplin showing a successful configuration.](images/joplin_check_sync.png "Hooray, all working!")

## Conclusion

Repeating these steps on any device you want Joplin on is fairly painless, and being able to have a Markdown-based editing environment everywhere is so very nice. The mobile app editing experience isn't as polished as it could be, but it's not a showstopper; just a mild annoyance.

On desktop, Joplin also works very well with external editors; I end up doing a lot of my note-taking and writing in [Typora][typora], a paid Markdown editor that offers a clean workspace while showing your formatting as you go. It works for me, and that's what's important!

If anything I've written about here sounds interesting, give it a try! You might find a new process you really like! :smile:


[obsidian]: https://obsidian.md/
[joplin]: https://joplinapp.org/
[joplincloud]: https://joplinapp.org/plans/
[webdav]: https://en.wikipedia.org/wiki/WebDAV
[fastmail]: https://fastmail.com
[fastmail_referral]: https://ref.fm/u27731032
[fastmail_webdav]: https://www.fastmail.help/hc/en-us/articles/1500000280121-About-Fastmail-file-storage
[typora]: https://typora.io/
