#!/usr/bin/env python3
""" Module of Authentication Class """
from flask import jsonify, abort, request
from api.v1.views import app_views
from typing import List, TypeVar
import re


class Auth():
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Validates excluded paths """
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if excluded_paths[-1] == '*':
                pat = excluded_paths.split('*')
                pat = pat[0] + '.*'
                match = re.search(pat, path)
                if match:
                    return False
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Validate all requests to secure the API """
        if not request or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user authentication """
        return None
