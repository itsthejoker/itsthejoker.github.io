# Gitea Actions, Python, and Debian


## Gitea Actions - the new self-hosted CI

{{< admonition type=warning title="Hey, you in the future!" >}}
I don't intend to update this as time goes on, so if you're reading this far from when it was written, just know that it might be out of date. Use your best judgement!
{{< /admonition >}}

As of the brand new Gitea 1.19.0, Gitea [finally has a built-in Actions system!][gitea-1.19.0-release-blog] It's intentionally very close to GitHub Actions, meaning that many of the yaml files you've carefully built up over the years will just work out of the box! And for the most part, that's what happens... but since this is a new system, there are always some rough spots.

In this case, the question is "what happens if you try to run the GitHub `setup-python` action on a Debian runner?"

> Tl;dr: it explodes in a very confusing way. Let's dive into that.

(Want to skip to the important bits? [Click here!](#the-problem))

## The Setup

I run Gitea on my local [Unraid][unraid] server in Docker, which has a single VM set aside to act as the runner. Actually getting the runner set up was pretty great - [the full instructions are here][gitea-act-runner-repo], but here's the basics.

On Gitea, you'll need to start by enabling Actions. This is deceptively simple, but does require editing the `app.ini` file. Just drop this anywhere in it:

```ini
[actions]
ENABLE = true
```

Restart Gitea and you should see a new option, `Runners`, in the Site Administration section.

![A screenshot showing part of the Gitea admin navbar; "Applications, Runners, Configuration".](images/gitea_runners_header.png "Should appear in this general location." )

After that, you're good to start on building the runner, and that general process is going to look like this:

* Build and update your VM
* Install Docker CE on the runner
* Grab the precompiled binary and drop it in the home folder

I renamed the precompiled binary to `act_runner` just to make the rest of the steps easy, but after [registering the runner][register-gitea-runner], you should be able to run it manually (`act-runner daemon`) and see it pop up in the Gitea runners list!

![A screenshot showing that Gitea has one idle runner.](images/gitea_runners.png "Awesome! One runner, ready and waiting for a job!")

At this point, there's only one more thing you have to do -- because this is still technically a beta feature, Actions have to be enabled on a _per-repo_ basis. Go to the repo that you want to test with and go to Settings > Repository > Advanced Settings. Buried in the many options there, you'll find this one for Actions -- enable it and click the save button at the bottom of the section.

![A screenshot showing the group of options that includes enabling Actions.](images/gitea_repo_actions_checkbox.png "Sometimes it's hard to find, but it'll be there.")

Now that we have all the pieces in place, we can finally test some actions! You should be able to use pretty much any GHA file (and Gitea will recognize files in both `.github/workflows/*.yaml` and `.gitea/workflows/*.yaml`), but start with a simple one. Since pretty the majority of my projects are in Python, I started with this existing release script for a Python-based system utility I wrote for myself:

```yaml
name: Release

on:
  push:
    branches:
    - master

jobs:
  build:
  runs-on: ubuntu-latest
  permissions:
    contents: write
  steps:
  - uses: https://github.com/actions/checkout@v2
  - name: lsb_release -i -r -s
    run: lsb_release -i -r -s
  - uses: https://github.com/actions/setup-python@v4
    with:
    python-version: '3.11.x'
  - name: Install Env
    # this should be all we need because shiv will download the deps itself
    run: |
      pip install --upgrade pip
      pip install shiv
      pip install poetry
  - name: Add CURRENT_TIME env property
    run: echo "CURRENT_TIME_VERSION=v$(date '+%s')" >> $GITHUB_ENV
  - name: Build the sucker
    run: |
      sed -i -e "s/?????/${{ env.CURRENT_TIME_VERSION }}/g" src/__init__.py
      make build
  - uses: https://github.com/ncipollo/release-action@v1
    with:
    artifacts: "utils"
    body: "It's releasin' time"
    generateReleaseNotes: false
    tag: ${{ env.CURRENT_TIME_VERSION }}
    commit: master
    token: ${{ secrets.PAT }}
```

You'll notice that there's only one change from a standard GHA file -- I've prepended `https://github.com/` to each step that uses an external action (and I'm not even 100% sure if that's needed, but that was in the examples so I'm rolling with it).

I also had to create a new secret -- since I use the Personal Access Token on GitHub added to the repo on GitHub, I went looking for a suitable replacement on Gitea. I'm very pleased to report that not only can repositories hold secrets (as expected) but you can assign secrets to your user account and they'll automatically apply to all your repos! I created a basic token with repository permissions and added it as a user secret called `PAT` -- that section of the run file works 100% as expected. Bravo, Gitea!

![A screenshot of the account Secrets page in Gitea.](images/gitea_secrets.png "Shh. It's a secret.")

When I went to run this with a push though, something interesting happened: it exploded on the "setting up Python" step, which I honestly expected to be fairly nondescript. What happened?

## The Problem

When debugging, the action failed with the following error:

```
##[debug]Unable to locate executable file: lsb_release. Please verify either the file path exists or the file can be found within a directory specified by the PATH environment variable. Also check the file mode to verify the file is executable.
```

Before we get too deep here, this is a **partial red herring**, but one that will eventually lead us to the real problem. The reason it's a red herring is that the error message is correct, but not for an obvious reason.

Debian doesn't ship with `lsb-release`, the package that will let you run the `lsb_release` command. (You can install it with `sudo apt install lsb-release`, but that still won't solve the issue.) What it's actually saying is that it can't find `lsb_release` _on the Docker container the runner downloaded_. For reasons I don't completely understand, this is not a problem that is solvable by simply installing `lsb-release` in an earlier step of your workflow file -- it'll still explode with the same error.

On your runner VM, in the directory where you registered `act_runner`, there is a hidden file called `.runner`. If you open that up, you'll see that there is a section called `labels`, and it (most likely) looks like this:

```json
"labels": [
  "ubuntu-latest:docker://node:16-bullseye",
  "ubuntu-22.04:docker://node:16-bullseye",
  "ubuntu-20.04:docker://node:16-bullseye",
  "ubuntu-18.04:docker://node:16-buster"
]
```

The `node:16` containers work well for _most_ things, but for some reason they don't work out of the box for this use case. What we can do is swap out these images for ones that _are_ configured correctly:

```json
"labels": [
  "ubuntu-latest:docker://catthehacker/ubuntu:act-latest",
  "ubuntu-22.04:docker://catthehacker/ubuntu:act-22.04",
  "ubuntu-20.04:docker://catthehacker/ubuntu:act-20.04",
  "ubuntu-18.04:docker://catthehacker/ubuntu:act-20.04"
]
```

After you change out the label section, restart the runner and then restart the job through the Gitea interface (or a push to your repo).

![A screenshot of a successful build on Gitea Actions.](images/gitea_build_success.png "Ignore the extra debug 'lsb_release' step!")

In a tremendously surprising move, even the release action worked out of the box, successfully pushing a release to my repo with no issues. Now I just have to fix the update checker (since the Gitea API isn't a 1:1 with GitHub's) and we're good to go!

Major props to the Gitea team for getting this out the door -- I'm so excited that it's here and very excited to use it on my repos!

[gitea-1.19.0-release-blog]: https://blog.gitea.io/2023/03/gitea-1.19.0-is-released/
[unraid]: https://unraid.net/
[gitea-act-runner-repo]: https://gitea.com/gitea/act_runner
[register-gitea-runner]: https://gitea.com/gitea/act_runner#quickstart
