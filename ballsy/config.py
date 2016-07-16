import configparser
import os
import re
import six
import stat
import subprocess

GITCONFIGLINE = re.compile('^([^=]+)=(.+)$')
GITREMOTEKEY = re.compile('^remote.([^.]+).url')


class Config(object):

    def _extract_github_repo(self, url):
        m = re.match("^git@github.com:([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+).git$",
                     url) or \
            re.match("^https://github.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)" +
                     ".git$", url)
        return (m.group(1), m.group(2)) if m else None

    def _get_remotes(self):
        self.remotes = {}
        for k, v in six.iteritems(self.gitcfg):
            m = GITREMOTEKEY.match(k)
            if m:
                self.remotes[m.group(1)] = self._extract_github_repo(v)

    def __init__(self):
        self.fn = os.path.join(os.path.expanduser('~'), '.ballsyrc')
        self.cfg = configparser.ConfigParser()
        self.gitcfg = {}
        if os.path.isfile(self.fn):
            self.cfg.read(self.fn)
        try:
            process = subprocess.Popen(["git", "config", "-l"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()
            for l in out.splitlines():
                m = GITCONFIGLINE.match(l.decode("utf-8"))
                if m:
                    self.gitcfg[m.group(1)] = m.group(2)
        except:
            pass
        self._get_remotes()

    def git_config(self, val):
        if val in self.gitcfg:
            return self.gitcfg[val]
        else:
            return None

    def has_token(self):
        if 'login' in self.cfg:
            if 'id' not in self.cfg['login'] or len(
                    self.cfg['login']['id']) == 0:
                return False
            if 'token' not in self.cfg['login'] or len(
                    self.cfg['login']['token']) == 0:
                return False
            return True
        else:
            return False

    def set_token(self, id, token):
        self.cfg['login'] = {'id': id, 'token': token}
        with open(self.fn, 'w+') as configfile:
            self.cfg.write(configfile)
        os.chmod(self.fn, stat.S_IRWXU)

    def token(self):
        if 'login' not in self.cfg:
            raise RuntimeError('No token found in ' + self.fn +
                               ", please run 'ballsy login'")
        else:
            return self.cfg['login']['token']

    def id(self):
        if 'login' not in self.cfg:
            raise RuntimeError('No token found in ' + self.fn +
                               ", please run 'ballsy login'")
        else:
            return self.cfg['login']['id']
