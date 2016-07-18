# ballsy
[![Latest version](https://img.shields.io/pypi/v/ballsy.svg)](https://pypi.python.org/pypi/ballsy)

[![License](https://img.shields.io/badge/Licence-Apache2-brightgreen.svg)](https://opensource.org/licenses/BSD-2-Clause)

[![Downloads](https://img.shields.io/pypi/dm/ballsy.svg)](https://pypi.python.org/pypi/ballsy)

Ballsy is a GitHub release tarball signing tool. It tries to promote signing of
the automatically generated release tarballs on GitHub with developer's OpenPGP
keys. Usually that would involve:

  - pushing a tag
  - navigating to the GitHub web page and creating a release
  - downloading their tarball
  - signing the tarball
  - uploading the detached ASCII signature to the release page as an asset

(And then redo this for the ZIP file...) The Debian wiki has a good set of
[instructions for this](https://wiki.debian.org/Creating%20signed%20GitHub%20releases).

Most of us probably wouldn't bother doing this. This software automates this
job by taking care of the necessary steps as outlined above.

Additional features:

  - Automatic conversion from tags to releases
  - Selective signing of ZIPs/tarballs
  - Automatic target repo selection based on current directory

# Installation

    $ pip install ballsy

# Usage

You'll need to log in to GitHub once:

    $ ballsy login

which will ask for your user credentials, and then obtain a token for future
logins (stored in `~/.ballsyrc`). 2FA by phone is supported.

After logging in, signing is as easy as:

    $ ballsy sign v2.0

to sign the release v2.0 in the GitHub repo pointed to by the `origin` remote
in the current directory (which is the default). Other targets can easily be
specified:

    $ ballsy sign --remote home v2.0
    $ ballsy sign --repo foobar/otherrepo v2.0

By default, the key specified
in Git's `user.signingkey` property is used, but this can be overridden using
the `--keyid` option.

If you don't usually use releases on GitHub, just tags, it is possible to
automatically prepare a release given a tag (`--include-tags`). This also works
when specifying multiple tags:

    $ ballsy sign --include-tags v1.0 v1.2 v2.0

Please see `ballsy --help` and `ballsy sign --help` for more options.

# TODO

At the moment you have to trust GitHub not to alter the contents of the
tarballs when preparing a release. Future versions of ballsy will verify the
contents of the downloaded tarballs against the local content corresponding to
given tags.

# LICENSE

2-clause BSD, see `LICENSE.txt`
