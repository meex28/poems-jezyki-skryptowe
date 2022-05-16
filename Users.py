from sqlalchemy.orm import sessionmaker
from security_databases import User, engine, Token
from Exceptions import *
from flask import request, render_template

import secrets
import string
import hmac
import hashlib
import base64


def generateRandomString(length):
    alphabet = string.ascii_letters + string.digits
    res = ''.join(secrets.choice(alphabet) for i in range(length))
    return res


def decodeToken(token):
    token = token.encode()
    token = base64.b64decode(token).decode()
    return token

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


class UsersService:
    def __init__(self):
        self.__dao = UsersDAO()

    def isLoginAvailable(self, login):
        user = self.__dao.getUserByLogin(login)
        return user is None

    def createNewUser(self, login, password):
        if not self.isLoginAvailable(login):
            raise ValueError("Login is already used")

        salt = generateSalt()
        password = hashPassword(password, salt)
        user = User(login, password, salt)

        # TODO: add exceptions
        self.__dao.addUser(user)

        return True

    # login to given account
    def login(self, login, password):
        # check password
        if not self.isPasswordCorrect(login, password):
            raise Unauthorized("Incorrect login or password")

        # TODO: return token value (when token service is added)
        return "token"

    # check if given password is correct for given account
    def isPasswordCorrect(self, login, password):
        user = self.__dao.getUserByLogin(login)

        if user is None:
            return False

        password = hashPassword(password, user.salt)

        return password == user.password


class UsersDAO:
    def __createSession(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def addUser(self, user):
        session = self.__createSession()

        session.add(user)
        session.commit()

    def deleteUserByLogin(self, login):
        session = self.__createSession()

        user = session.query(User).get(login)
        session.delete(user)
        session.commit()

    def deleteUser(self, user):
        session = self.__createSession()

        session.delete(user)
        session.commit()

    def getUserByLogin(self, login):
        session = self.__createSession()

        user = session.query(User).get(login)
        return user

    def updatePassword(self, login, newPassword):
        session = self.__createSession()
        user = session.query(User).get(login)
        user.password = newPassword
        session.flush()
        session.commit()

    def saveToken(self, token):
        session = self.__createSession()
        session.add(token)
        session.commit()


class UsersController:
    __service = UsersService()

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            return 'POST LOGIN'

    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            print(request.form)
            return 'POST REGISTER'


if __name__ == '__main__':
    service = UsersService()
    token = generateToken("login")
    print(token)
    print(decodeToken(token))
    # print(service.decodeToken(token))
