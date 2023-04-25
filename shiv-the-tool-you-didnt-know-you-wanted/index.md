# shiv - the Python Tool You Didn't Know You Wanted


## Your code + a zip archive = single file deployments

I know that's an incredibly enticing intro, but bear with me. We'll get there.

## Zip archives?

Way back in the dark ages of 2008, **Python 2.6** was released. This release was particularly exciting because it brought us such wondrous things as the [`multiprocessing` module][multiprocessing_std_lib], the [`io` module][io_std_lib], and codified the [`with` statement][with_statement] as a keyword for doing better-controlled contextual processing. It also brought a lot of existential angst about the upcoming Python 3 release, but we're skipping over that.

Buried in the release notes was a single paragraph that mentioned ["oh hey by the way you can now run Python files from inside a zip archive"][zip2.6].

{{< image src="/gifs/samueljackson-what.gif" alt="Samuel Jackson in the movie _Coming to America_ saying 'WHAT?!' incredulously." caption="This is a pretty accurate representation of how I felt reading this in the future." >}}

Imagine, being able to call a zip file with Python and have it actually work:

```sh
# You don't have to imagine. This works.
❯ echo "print('hello, world!')" >> __main__.py

❯ zip test.zip __main__.py                 
  adding: __main__.py (stored 0%)

❯ python test.zip
Hello, World!
```

This was, somewhat predictably, completely missed by the vast majority of folks. In [2013, PEP 441][pep441] attempted to fix this by bringing the whole 'package your stuff in a zip file' thing into the public view by [adding the `zipapp` module][zipapp_std_lib] to the standard library, adding a whole suite of tools to make working with zipapps much easier for the average Python developer.

This was such a revolutionary change that it [got a whole three sentences][zipapp_release_notes] in the release notes and was more or less completely overshadowed by the [introduction of `typing`][typing_std_lib] as a core Python feature. Sorry, [Daniel and Paul][pep441] -- you tried.

Now that we have reasonable support for making and using zipapps, we can cover the single huge glaring issue: **no third-party dependencies**.

## The Problem

Zipapps are fantastic! They let you bundle ALL of your Python code into a single zip archive, pass that archive off to someone else, and they can _just run it_! However, there's one glaring issue: **you can only rely on the standard library**. Third party dependencies are right out unless you manually bundle them with your codebase, which is both a pain to do in the first place and an easy way to accidentally run afoul of licenses if you're not paying close enough attention.

I don't know about you, but I basically never write things that rely _only_ on the standard library -- third party dependencies are a fact of life for all the Python developers I know. So how can we get the power of third party dependencies with the pure awesomeness of being able to package an entire runnable program into a zip file?

The answer, as it turns out, was figured out by all those cool folks at Twitter who aren't there anymore. They [designed and built `pex`][pex], a system that solves the third party dependency problem by essentially zipping up the virtual environment (minus the interpreter) and extracting it prior to running the zipapp. The implementation used by `pex` is functional, though a bit on the slow side.

`shiv` is LinkedIn's attempt at solving the speed issues of `pex` while still keeping all of the functionality. (You can find more information about the [speed differences between `pex` and `shiv` here.][pex_speed_comparison] You can also find more technical information on `shiv`'s approach at that link as well.) You only need a few things installed to actually make a `shiv` app:

* a recent version of Python
* an environment that includes `shiv`
* a setup.py file that lists all the dependencies of your app
* your app code itself

That's really it, and in fact, that's all you need to have in your CI pipeline if you want to automatically build your `shiv` apps for CI-controlled releases. Take a look at this example, starting from an empty directory:

```sh
# we need a virtual environment to start in.
❯ python -m venv .venv

❯ . .venv/bin/activate

# Now that we have an environment to work in,
# we'll install shiv.
❯ pip install shiv
Collecting shiv
  Using cached shiv-1.0.3-py2.py3-none-any.whl (19 kB)
Collecting click!=7.0,>=6.7 (from shiv)
  Using cached click-8.1.3-py3-none-any.whl (96 kB)
Requirement already satisfied: pip>=9.0.3 in ./.venv/lib/python3.11/site-packages (from shiv) (23.1.1)
Requirement already satisfied: setuptools in ./.venv/lib/python3.11/site-packages (from shiv) (65.5.0)
Installing collected packages: click, shiv
Successfully installed click-8.1.3 shiv-1.0.3

# Cool. Let's make our app.
❯ mkdir myapp
❯ echo "import httpx\ndef main():\n    print(httpx.get)" >> myapp/cli.py
❯ touch myapp/__init__.py
```
We have a single file that calls a third-party dependency and attempts to print a reference. If we call it now with `python cli.py` it'll break, since we don't have `httpx` installed. However, we'll add a reference to that in our setup.py file now.

```sh
❯ touch setup.py
❯ tee -a setup.py <<EOF
∙ from setuptools import setup
∙ setup_kwargs = {
∙   'name': 'myapp',
∙   'version': '0.0.1', 
∙   'packages': ['myapp'],
∙   'install_requires': ['httpx'],       
∙   'entry_points': {'console_scripts': ['myapp = myapp.cli:main']},
∙   'python_requires': '>=3.10' 
∙ }
∙ setup(**setup_kwargs)
∙ EOF
from setuptools import setup
setup_kwargs = {
  'name': 'myapp',
  'version': '0.0.1', 
  'packages': ['myapp'],
  'install_requires': ['httpx'],       
  'entry_points': {'console_scripts': ['myapp = myapp.cli:main']},
  'python_requires': '>=3.10' 
}
setup(**setup_kwargs)
```

Now that we have a pretty basic `setup.py` file and everything else configured, we can make the app:

```sh
❯ shiv -c myapp -o myapp.pyz .
Processing /home/joe/code/test
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting httpx (from myapp==0.0.1)
  Downloading httpx-0.24.0-py3-none-any.whl (75 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 75.3/75.3 kB 1.6 MB/s eta 0:00:00
Collecting certifi (from httpx->myapp==0.0.1)
  Using cached certifi-2022.12.7-py3-none-any.whl (155 kB)
Collecting httpcore<0.18.0,>=0.15.0 (from httpx->myapp==0.0.1)
  Downloading httpcore-0.17.0-py3-none-any.whl (70 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 70.6/70.6 kB 3.1 MB/s eta 0:00:00
Collecting idna (from httpx->myapp==0.0.1)
  Using cached idna-3.4-py3-none-any.whl (61 kB)
Collecting sniffio (from httpx->myapp==0.0.1)
  Using cached sniffio-1.3.0-py3-none-any.whl (10 kB)
Collecting h11<0.15,>=0.13 (from httpcore<0.18.0,>=0.15.0->httpx->myapp==0.0.1)
  Using cached h11-0.14.0-py3-none-any.whl (58 kB)
Collecting anyio<5.0,>=3.0 (from httpcore<0.18.0,>=0.15.0->httpx->myapp==0.0.1)
  Using cached anyio-3.6.2-py3-none-any.whl (80 kB)
Building wheels for collected packages: myapp
  Building wheel for myapp (pyproject.toml): started
  Building wheel for myapp (pyproject.toml): finished with status 'done'
  Created wheel for myapp: filename=myapp-0.0.1-py3-none-any.whl size=1530 sha256=ad70a73161c189da712904a74056c663318f636e60ac3f8c5e4c869eeabde259
  Stored in directory: /tmp/pip-ephem-wheel-cache-1udsfhau/wheels/99/3a/8b/6471545a346414b14f2840e683b284e596ec400c771b147d19
Successfully built myapp
Installing collected packages: sniffio, idna, h11, certifi, anyio, httpcore, httpx, myapp
Successfully installed anyio-3.6.2 certifi-2022.12.7 h11-0.14.0 httpcore-0.17.0 httpx-0.24.0 idna-3.4 myapp-0.0.1 sniffio-1.3.0
```

If we check our directory, we have a new file -- `myapp.pyz`. Let's run it!

```sh
❯ python myapp.pyz
<function get at 0x7f41d3a64360>
```

Now we have a single zip archive that includes a third party dependency that can be referenced and interacted with! It printed the reference to `httpx`, so we know that it's in there.

...actually, do we know it's in there? Maybe it's just picking that up from the environment that's still activated. Let's check.

```sh
❯ deactivate

# oh yeah, and you can totally call it directly
# instead of using `python myapp.pyz`!
❯ ./myapp.pyz
<function get at 0x7f368c70ade0>

# Let's check real quick to make sure httpx
# isn't lurking somewhere on the system path.
❯ python -c "import httpx"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'httpx'
```

There we go! We can see that it's pulling the dependency from its own packaged virtual environment.

## The Use Case

Being able to package your entire app into a zip file has some incredible benefits, namely that you can now run your entire app on any system that just has an appropriate version of Python installed. For applications where your app just needs to run without tweaking, this means that someone (or something) can just grab your compiled and finished zipapp and just... run it. No fuss and no stress.

{{< admonition type=warning title="Okay, maybe not quite 'no fuss'." >}}
You'll want to make sure that you're 'compiling' on the same type of OS that you're deploying to if you're bundling any compiled C extensions. Regular Python code should be totally fine.
{{< /admonition >}}

I wouldn't recommend that you check this out unless I'd given it a thorough test myself; the nonprofit I run, [the Grafeas Group][gg], has been running **all of our production services** as zipapps for the last 8 months. That's:

* [three][tor] [Reddit][tor_ocr] [bots][tor_archivist]
* a [Discord bot][buttercup]
* a [Slack bot][bubbles]
* a [Django monolith][blossom] that handles our website and APIs

Deployments have never been easier (and are [completely controlled via Slack commands!][gg_deployment]) -- it's literally as easy as backing up the existing zipapp, downloading the new one, and running it. The Slack bot, [Bubbles][bubbles], updates itself by downloading the new version on top of the existing one and restarting its own service!

The benefit here is that if the new version fails, getting back to a working state just swapping out the older version of the zipapp and restarting the service. What's that? You made changes to the virtual environment between versions? Doesn't matter because each zipapp uses its own environment. If it compiles and it works, it can't be affected by any other zipapp, even later or earlier compilations of the same system.

Spinning up a new server is as easy as getting a new VM, installing Python on it, and slapping the zipapps into place with their respective environment variable files. We intentionally keep it simple because this is a volunteer gig and there's no reason to muddy the devops waters by adding something like Docker. But let's say _you_ wanted to add Docker or another container; would that be any more complex?

Honestly, not really. You'd basically just get the official Python container, drop your zipapp onto the root and set your launch script to call it. It does kind of defeat the purpose of easy updates, but it can be done!

## Stuff to Watch For

As cool as using `shiv` for easily-deployable apps is, there are a few things that you need to know if you want to use it in production.

### Abandoned Environments

`shiv` puts the virtual environment for that zipapp in `~/.shiv` unless you override it, and since each zipapp (and each version of each zipapp) has its own virtual environment, that means that this directory can get reasonably busy. The easiest way to address this is to use the "preamble" section of `shiv`'s setup, which allows you to run a single script before actually starting the zipapp.

There's a complete preamble script that handles abandoned environments [available in the `shiv` documentation][environment_cleanup] -- adding and extending it is pretty straightforward, but it is something that you need to be aware of as environments can build up across deployments.

### Path() Shenanigans

The only other major thing you need to watch out for is **relative paths**. Let's edit our `cli.py` file:

```python
import os
import pathlib

def main():
    print(os.getcwd())
    print(pathlib.Path(__file__))

if __name__ == "__main__":
    main()
```

If we run this directly with `python myapp/cli.py`, here's what I get:

```sh
❯ python myapp/cli.py
/home/joe/code/test
/home/joe/code/test/myapp/cli.py
```

But if we compile this into a zipapp, things will look a little different:

```sh
❯ shiv -c myapp -o myapp.pyz .
Processing /home/joe/code/test
...

❯ ./myapp.pyz
/home/joe/code/test
/home/joe/.shiv/myapp.pyz_c1a18b172051ba68db2091f324e067c2e9c6b74dad677c71f3748348c2b376d6/site-packages/myapp/cli.py
```

...which is _not_ where we expected it to be. That means that if you want to load external files that are in the same directory as the compiled zipapp (and `os.getcwd()` might not be accurate for your use case), you'll need to ask shiv itself where you're running. Thankfully, there's an extra little bit that gets injected into the final zipapp during build time, and there are a couple of utilities there that can help us out.

Let's rebuild our script a little bit -- now we'll do a check to see if `shiv` is available in the current environment and then print out the directory that our zipapp is in. This would be useful anytime you want to load external files in the same directory, like a `.env` file, a `db.sqlite3` file, or something else along those lines.

Here's the new `cli.py` file:

```python
import os
from pathlib import Path

try:
    from shiv.bootstrap import current_zipfile
    IN_SHIV = True
except ImportError:
    IN_SHIV = False

def main():
    print(f"Calling from {os.getcwd()}...")
    if not IN_SHIV:
        print("shiv is not installed.")
        print(Path(__file__).parent.parent)
    else:
        with current_zipfile() as archive:
            if archive:
                print("shiv is installed and we are inside a zipapp!")
                print(Path(archive.filename).resolve(strict=True).parent)
            else:
                print("shiv is installed and we are NOT in a zipapp!")
                print(Path(__file__).resolve(strict=True).parent.parent)

if __name__ == "__main__":
  main()
```

Now, let's try running it!

```sh
# outside the environment, calling directly:
❯ python myapp/cli.py
Calling from /home/joe/code/test...
shiv is not installed.
/home/joe/code/test

# inside the environment, calling directly:
❯ python myapp/cli.py
Calling from /home/joe/code/test...
shiv is installed and we are NOT in a zipapp!
/home/joe/code/test

# calling the zipapp:
❯ ./myapp.pyz
Calling from /home/joe/code/test...
shiv is installed and we are inside a zipapp!
/home/joe/code/test
```

We use this method to create a `BASE_DIR` variable that's accessible throughout the application along the lines of Django's BASE_DIR (which is _very_ wrong when packaged with `shiv`). That allows easy loading of external files and makes it work the way you expect it to. A little bit of boilerplate, but nothing too bad once you know to watch for it.

## Conclusion

If you're looking for a low-tech way to deploy a single python app (or a BUNCH of them!) or just want to pass scripts and things around to coworkers, `shiv` is worth your time to check out. Coupled with building and releasing the zipapps in your CI pipeline, it's a system that is really hard to beat. Usability is great, using it is a snap, and if you pair it with `click`, you can get extremely usable CLI programs for essentially no cost.

The linked repositories in this post are a great place to look if you're wanting to see what this looks like in practice, and you can also take a look at my [self-updating utils script here][utils] if you'd like to see how `click` can be used to add an easy `--update` flag that checks for a new release and automatically installs it!

Happy packaging!

<!-- links -->

[multiprocessing_std_lib]: https://docs.python.org/3/library/multiprocessing.html
[io_std_lib]: https://docs.python.org/3/library/io.html
[with_statement]: https://docs.python.org/2/reference/compound_stmts.html#with
[zip2.6]: https://docs.python.org/2/whatsnew/2.6.html#other-language-changes
[pep441]: https://peps.python.org/pep-0441/
[zipapp_std_lib]: https://docs.python.org/3/library/zipapp.html
[zipapp_release_notes]: https://docs.python.org/3/whatsnew/3.5.html#zipapp
[typing_std_lib]: https://docs.python.org/3/library/typing.html
[pex]: https://pex.readthedocs.io/
[pex_speed_comparison]: https://shiv.readthedocs.io/en/latest/history.html#how
[gg]: https://grafeas.org
[bubbles]: https://github.com/grafeasgroup/bubbles
[gg_deployment]: https://github.com/GrafeasGroup/Bubbles/blob/main/bubbles/commands/deploy.py
[buttercup]: https://github.com/grafeasgroup/buttercup
[blossom]: https://github.com/grafeasgroup/blossom
[tor]: https://github.com/grafeasgroup/tor
[tor_ocr]: https://github.com/grafeasgroup/tor_ocr
[tor_archivist]: https://github.com/grafeasgroup/tor_archivist
[environment_cleanup]: https://shiv.readthedocs.io/en/latest/index.html#preamble
[utils]: https://git.joekaufeld.com/jkaufeld/utils
