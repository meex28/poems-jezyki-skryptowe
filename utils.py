import secrets
import string
import hmac
import hashlib
import base64

from enum import Enum
from sqlalchemy.orm import sessionmaker
from databases import engine


class DAO:
    def __createSession(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def add(self, value, session=None):
        if session is None:
            session = self.__createSession()

        session.add(value)
        session.commit()

    def delete(self, value, session=None):
        if session is None:
            session = self.__createSession()

        session.delete(value)
        session.commit()


def generateRandomString(length):
    alphabet = string.ascii_letters + string.digits
    res = ''.join(secrets.choice(alphabet) for i in range(length))
    return res


def decodeToken(token):
    token = token.encode()
    token = base64.b64decode(token).decode()
    return tuple(token.split(':'))


# generate token in format {random string of 32 length}:{login}
def generateToken(login):
    token = f'{generateRandomString(32)}:{login}'.encode()
    token = base64.b64encode(token).decode()
    return token


def generateSalt():
    return generateRandomString(8)


def hashPassword(password, salt):
    password = password.encode()
    salt = salt.encode()

    return hmac.new(password, salt, hashlib.sha256).hexdigest()
