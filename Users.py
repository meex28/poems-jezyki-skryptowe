from sqlalchemy.orm import sessionmaker
from security_databases import User, engine
import secrets
import string
import os
import hmac
import hashlib
import binascii


def generateSalt():
    alphabet = string.ascii_letters + string.digits
    salt = ''.join(secrets.choice(alphabet) for i in range(8))
    return salt


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


if __name__ == '__main__':
    dao = UsersDAO()
    service = UsersService()
    # dao.addUser(User("user1", "pass1", "salt1"))
    # dao.addUser(User("user2", "pass2", "salt2"))
    # dao.addUser(User("user3", "pass3", "salt3"))
    # print(dao.getUserByLogin('user1'))
    # dao.updatePassword('user1', 'newpassword1')
    # print(dao.getUserByLogin('user1'))
    service.createNewUser("newuser", "newpassword")
