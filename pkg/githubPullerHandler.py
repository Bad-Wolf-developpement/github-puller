import os
import sys
import functools
import json
from os import path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from gateway_addon import APIHandler, APIResponse, Database

print = functools.,partial(print, flush=True)