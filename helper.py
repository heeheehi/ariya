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


# class DTResponse(Response):
#     charset = 'utf-8'
#     default_status = 200
#     default_mimetype = 'application/json'
#
#     @classmethod
#     def force_type(cls, rv, environ=None):
#         if isinstance(rv, (str, int, dict, list)):
#             rv = jsonify(rv)
#         elif isinstance(rv, ErrorResponse):
#             rv = response_error(exception=rv, debug=mode.lower() != 'production', log_file=None if not mode else '')
#         return super(DTResponse, cls).force_type(rv, environ)
#
#
# def create_hash_from_user(user):
#     return hashlib.md5("{}{}{}{}".format(user['password'] if user['password'] else '',
#                                          user['pwHash'] if user['pwHash'] else '',
#                                          user['email'] if user['email'] else '',
#                                          user['fb_id'] if user['fb_id'] else '').encode('utf-8')).hexdigest()
#
#
# def response_ok(additional_data):
#     json_str = json.dumps(additional_data, ensure_ascii=False).encode('utf-8').decode('utf-8')
#
#     response = make_response(json_str, 200)
#     response.headers['Content-Type'] = 'application/json; charset=utf-8'
#
#     return response
#
#
# # TODO: Test code for multi-lang logging
# # JWT check decorator
# def lang_check(func):
#     @wraps(func)
#     def decorated_func(*args, **kwargs):
#         request.lang = request.headers.get('Accept-Language', 'ko')
#         if request.lang not in ['en', 'ko', 'zh', 'jp']:
#             request.lang = 'ko'
#
#         return func(*args, **kwargs)
#
#     return decorated_func
#
#
# # 에러 처리 시
# @lang_check
# def response_error(err):
#     return make_response(jsonify({
#         'state': err.code,
#         'message': err.msg('ko'),
#         'data': err.data
#     }), err.status_code)
#
#
# def response_err(state, message, data=None, http_status_code=406):
#     return make_response(jsonify({
#         'state': state,
#         'message': message,
#         'data': data
#     }), http_status_code)
#
#
# def front_version_gte(version='4.6.0'):
#     x_version = request.headers.get('X-Version', None)
#     return x_version and StrictVersion(version) < StrictVersion(x_version)
#
#
# def front_version_lte(version='4.6.0'):
#     x_version = request.headers.get('X-Version', None)
#     return not x_version or (x_version and (StrictVersion(version) >= StrictVersion(x_version)))
