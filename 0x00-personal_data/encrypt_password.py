#!/usr/bin/env python3
""" Password Encryption module """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function to Hash a password for the first time,
    with a randomly-generated salt

    Argument:
    password: string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check that an unhashed password matches one that has previously been hashed

    Arguments:
    hashed_password: bytes
    password: string
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
