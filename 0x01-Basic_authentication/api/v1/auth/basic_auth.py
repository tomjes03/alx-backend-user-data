#!/usr/bin/env python3
""" Module of Basic Authentication Class """
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from typing import List, TypeVar
import base64
import re


class BasicAuth(Auth):
    """ Class to manage the API basic authentication """

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ Validate all requests to secure the API """
        if authorization_header and type(authorization_header) is str:
            if re.match("^Basic\s", authorization_header):
                return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header:
            if type(base64_authorization_header) is str:
                try:
                    decoded = base64.b64decode(base64_authorization_header)
                    return decoded.decode('utf-8')
                except Exception:
                    return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is str:
                details = decoded_base64_authorization_header.split(":", 1)
                if len(details) > 1:
                    return (details[0], details[1])
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if not user_email and not user_pwd:
            if type(user_email) is not str and type(user_pwd) is not str:
                return None
        from models.user import User
        users = User.search({"email": user_email})
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        auth = BasicAuth()
        b64_auth = None
        b64_decoded = None
        user_cred = None
        usr = None
        auth_header = self.authorization_header(request)
        if auth_header:
            b64_auth = auth.extract_base64_authorization_header(auth_header)
        if b64_auth:
            b64_decoded = auth.decode_base64_authorization_header(b64_auth)
        if b64_decoded:
            user_cred = auth.extract_user_credentials(b64_decoded)
        if user_cred:
            usr = auth.user_object_from_credentials(user_cred[0], user_cred[1])
        print(usr)
        return usr
