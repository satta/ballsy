import configparser
import os
import stat

class Config(object):
    def __init__(self):
        self.fn = os.path.join(os.path.expanduser('~'),'.ballsyrc')
        self.cfg = configparser.ConfigParser()
        if os.path.isfile(self.fn):
            self.cfg.read(self.fn)

    def logged_in(self):
        return ('login' in self.cfg)

    def set_token(self, id, token):
        self.cfg['login'] = {'id': id, 'token': token}
        with open(self.fn, 'w+') as configfile:
            self.cfg.write(configfile)
        os.chmod(self.fn, stat.S_IRWXU)

    def token(self):
        if not 'login' in self.cfg:
            raise RuntimeError('No token found in ' + self.fn +
                ", please run 'ballsy login'")
        else:
            return self.cfg['login']['token']

    def id(self):
        if not 'login' in self.cfg:
            raise RuntimeError('No token found in ' + self.fn +
                ", please run 'ballsy login'")
        else:
            return self.cfg['login']['id']
