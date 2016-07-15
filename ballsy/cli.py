import github3
import click
import re
import sys
import ballsy.options
import ballsy.config

@click.group()
@click.option('--verbose', '-v', is_flag=True,
              help="Be verbose.")
@click.pass_context
def main(ctx, verbose):
    """GitHub release signing tool"""
    ctx.verbose = verbose
    pass

@main.command()
@click.option('--only-zip', '-z', is_flag=True,
              cls=ballsy.options.MutuallyExclusiveOption,
              help='Only sign the ZIP archive for release.',
              mutually_exclusive=["only-targz"])
@click.option('--only-targz', '-g' , is_flag=True,
              cls=ballsy.options.MutuallyExclusiveOption,
              help='Only sign the tarball for release.',
              mutually_exclusive=["only-zip"])
@click.option('--include-tags', '-t', is_flag=True,
              help='Draft release for tag if not present.')
@click.option('--no-draft', '-d', is_flag=True,
              help='Do not set draft flag for new releases.')
@click.option('--repo', required=True,
              help='Repository to sign releases for.')
@click.argument('tag', nargs=-1)
@click.pass_context
def sign(ctx, only_zip, only_targz, include_tags, no_draft, repo, tag):
    """Sign release(s)."""
    c = ballsy.config.Config()
    p = re.compile('([^/]+)/(.+)')
    m = p.match(repo)
    if m:
        ruser = m.group(1)
        rrepo = m.group(2)
    else:
        print('Invalid repository name: ' + repo)
        sys.exit(1)
    try:
        gh = github3.login(token=c.token())
        repo = gh.repository(ruser, rrepo)
    except Exception as e:
        print(str(e))
        sys.exit(1)

    #print("tags")
    #print(repo.ref('tags/' + tag))

    print("releases")
    for r in repo.releases():
      print(str(r))
      print(r.archive("tarball"))
      for a in r.assets():
        print(a.name)
        a.delete()
      r.upload_asset('text/ascii', "v2.0.0.tar.gz.asc", open('foo.sig'))
      for a in r.assets():
        print("-- " + str(a))

@main.command()
@click.pass_context
def login(ctx):
    """Log into GitHub and store user credentials."""
    import getpass
    c = ballsy.config.Config()

    try:
        prompt = raw_input
    except NameError:
        prompt = input

    user = ''
    while not user:
       user = prompt('GitHub username: ')

    pwd = ''
    while not pwd:
        pwd = getpass.getpass('GitHub password for {0}: '.format(user))

    def twofa_auth():
        code = ''
        while not code:
            code = prompt('Enter 2FA code: ')
        return code

    try:
        g = github3.login(user, pwd, two_factor_callback=twofa_auth)
        if c.logged_in():
            a = g.authorization(c.id())
            print(a)
        auth = g.authorize(user, pwd, ['user', 'repo'], "Ballsy")
        c.set_token(auth.id, auth.token)
    except Exception as e:
        print(str(e))
        sys.exit(1)

@main.command()
@click.pass_context
def logout(ctx):
    """Log out of GitHub."""
    c = ballsy.config.Config()
