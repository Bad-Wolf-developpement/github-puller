import os
import sys
import functools
import json
import subprocess
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

if __name__ == '__main__':
    liste = []
    _ADDONS_PATH = [
        os.path.join(os.path.expanduser('~'), '.webthings', 'addons'),
        ]

    if 'WEBTHINGS_HOME' in os.environ:
        _ADDONS_PATH.insert(0, os.path.join(os.environ['WEBTHINGS_HOME'], 'addons'))
    _ADDONS_PATH = _ADDONS_PATH[0]
    git_folder = GithubAPIHandler.get_git_folder("")
    print(git_folder)
   