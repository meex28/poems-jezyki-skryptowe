from sqlalchemy.orm import sessionmaker
from db import *

# base dao class, used for create and delete operations
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


class WorksDAO(DAO):
    pass