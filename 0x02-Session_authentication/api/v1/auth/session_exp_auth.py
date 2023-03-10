#!/usr/bin/env python3
""" Module of Basic Authentication Class """

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Class to manage the API session authentication expiration """

    def __init__(self):
        """ Initializing Class object """
        self.session_duration = 0
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            pass

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = {'user_id': user_id,
                                  'created_at': datetime.now()}
            self.user_id_by_session_id[session_id] = session_dictionary
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID """
        if not session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary:
            user = session_dictionary.get('user_id')
            if user:
                if self.session_duration <= 0:
                    return user
                created_at = session_dictionary.get('created_at')
                if created_at is None:
                    return None
                if (created_at + timedelta(seconds=self.session_duration) <
                        datetime.now()):
                    return None
                return user
