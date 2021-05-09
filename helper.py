import hashlib
import json
import os
from distutils.version import StrictVersion
from functools import wraps
from typing import cast

import flask
from flask import Request
from flask import request, make_response, jsonify, Response


class DTRequest(Request):
    def __init__(self, *args, **kwargs):
        super(DTRequest, self).__init__(*args, **kwargs)
        # this variables can be injected by API decorator.
        # define these variables for type hinting.

        self.connection = None

        self.user = None
        self.user_public = None

        self.lang = None


request: DTRequest = cast(DTRequest, flask.request)

mode = os.environ.get('ENV')

