from sqlalchemy.orm import sessionmaker
from databases import User, engine, Token
from Exceptions import *
from flask import request, render_template
from utils import *


class UsersService:
    def __init__(self):
        self.__dao = UsersDAO()

    # check if login is already used
    def isLoginAvailable(self, login):
        user = self.__dao.getUserByLogin(login)
        return user is None

    def createNewUser(self, login, password):
        if not self.isLoginAvailable(login):
            raise ValueError("Login is already used")

        # prepare password and save user in DB
        salt = generateSalt()
        password = hashPassword(password, salt)
        user = User(login, password, salt)

        # TODO: add exceptions
        self.__dao.add(user)

        return True

    # login to given account
    def login(self, login, password):
        # check password
        if not self.isPasswordCorrect(login, password):
            raise Unauthorized("Incorrect login or password")

        # generate and save token
        token = generateToken(login)
        self.__dao.add(token)

        return token

    # check if given password is correct for given account
    def isPasswordCorrect(self, login, password):
        user = self.__dao.getUserByLogin(login)

        if user is None:
            return False

        password = hashPassword(password, user.salt)

        return password == user.password


class UsersDAO(DAO):
    def deleteUserByLogin(self, login):
        session = self.__createSession()

        user = session.query(User).get(login)
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


class UsersController:
    __service = UsersService()

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            print(request.form)
            return 'POST LOGIN'

    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            print(request.form)
            return 'POST REGISTER'


if __name__ == '__main__':
    # service = UsersService()
    # service.createNewUser('orzel11', 'orzel')
    dao = UsersDAO()
    print(dao.getUserByLogin('orzel11'))
    # token = generateToken("login")
    # print(token)
    # print(decodeToken(token))
    # print(service.decodeToken(token))
