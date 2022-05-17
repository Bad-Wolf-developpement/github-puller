import os
import sys
import functools
import json
import subprocess
import requests
from os import path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from gateway_addon import APIHandler, APIResponse, Database

print = functools.partial(print, flush=True)

_ADDONS_PATH = [
    os.path.join(os.path.expanduser('~'), '.webthings', 'addons'),
]

if 'WEBTHINGS_HOME' in os.environ:
    _ADDONS_PATH.insert(0, os.path.join(os.environ['WEBTHINGS_HOME'], 'addons'))

_ADDONS_PATH = _ADDONS_PATH[0]

class GithubAPIHandler(APIHandler):

    def __init__(self, verbose = True):
        self.addon_name = 'github-puller'
        self.running = True
        self.ready = False

        self.api_server = 'http://127.0.0.1:8080'
        
        self.configs = self.load_db_config(self.addon_name)

        self.verbose = configs['debugMode']

        try:
            print("Trying my best")
            manifest_fname = os.path.join(
                os.path.dirname(__file__),
                '..',
                'manifest.json'
            )

            with open(manifest_fname, 'rt') as f:
                manifest = json.load(f)
                if self.verbose:
                    print(manifest)
                    
            super().__init__(manifest['id'], verbose=self.verbose)
            self.manager_proxy.add_api_handler(self)

            if self.verbose:
                print("self.manager_proxy = " + str(self.manager_proxy))
                print("Created new API HANDLER: " + str(manifest['id']))

        except Exception as e:
            print("Failed to init ux extension API handler: " + str(e))
        self.ready = True


    def load_db_config(self, package_name):
        """
        Load configuration from DB
        package_name -- name of the package as shown in the manifest.json
        Return the config object as dict
        """
        database = Database(package_name)
        if not database.open():
            print("Can't open database for package: {0}".format(package_name))
            return
        configs = database.load_config()
        database.close()

        return configs

    def get_git_folder(self):
        dirList = []
        for name in os.listdir(_ADDONS_PATH):
            if os.path.isdir(os.path.join(_ADDONS_PATH, name)):
                if '.git' in os.listdir(
                    os.path.join(_ADDONS_PATH, name)):
                    dirList.append(name)
        return dirList

    def get_github_branchs(self, url):
        listFromURL = url.split('/')
        branches= []
        repo = listFromURL[len(listFromURL) - 1]
        if len(repo.split('.'))  != 2:
            return False
        else:
            repo = repo.split('.')
            if repo[1] != 'git':
                return False
            else:
                repo = repo[0]
        user = listFromURL[len(listFromURL) - 2]
        gitAPIUrl = f'https://api.github.com/repos/{user}/{repo}/branches'
        response = requests.get(gitAPIUrl)
        if response.status_code != 200:
            return False

        datas = json.loads(response.text)
        for entry in datas:
            branches.append(entry['name'])

        github_branches = f'{branches}'
        return github_branches

if __name__ == '__main__':
    liste = []
    _ADDONS_PATH = [
        os.path.join(os.path.expanduser('~'), '.webthings', 'addons'),
        ]

    if 'WEBTHINGS_HOME' in os.environ:
        _ADDONS_PATH.insert(0, os.path.join(os.environ['WEBTHINGS_HOME'], 'addons'))
    _ADDONS_PATH = _ADDONS_PATH[0]
    github_branchs = GithubAPIHandler.get_github_branchs("", 'https://github.com/arist0v/sinope-out-temp.git')
    print(github_branchs)  