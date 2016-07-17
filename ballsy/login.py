import getpass
import github3


def login_with_password():
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

    g = github3.login(user, pwd, two_factor_callback=twofa_auth)
    return g, user, pwd


def login_with_token(token):
    g = github3.login(token=token)
    return g


def logout(github, config):
    if config.has_token():
        a = github.authorization(config.id())
        a.delete()
    config.cfg['login'] = None
