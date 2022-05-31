from DAOs import *
from utils import *
from exceptions import *


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
        self.__dao.addUser(user)

        return True

    # login to given account
    def login(self, login, password):
        # check password
        if not self.isPasswordCorrect(login, password):
            raise Unauthorized("Incorrect login or password")

        # generate and save token
        token = generateToken(login)
        tokenObj = Token(token)
        self.__dao.addToken(tokenObj)

        return token

    # check if given password is correct for given account
    def isPasswordCorrect(self, login, password):
        user = self.__dao.getUserByLogin(login)

        if user is None:
            return False

        password = hashPassword(password, user.salt)

        return password == user.password

    # check if given token is valid
    # return (boolean, string) : (is token valid, login)
    def checkToken(self, token):
        # token is Token object
        token = self.__dao.getToken(token)

        isTokenValid = token is not None
        user = None

        if isTokenValid:
            token, user = decodeToken(token.token)

        return isTokenValid, user


class WorksService:
    pass
