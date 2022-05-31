from sqlalchemy.orm import sessionmaker
from db import *


# base dao class, used for create, delete and get operations
class DAO:
    def _createSession(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def _add(self, value, session=None):
        if session is None:
            session = self._createSession()

        session.add(value)
        session.commit()

    def _delete(self, value, session=None):
        if session is None:
            session = self._createSession()

        session.delete(value)
        session.commit()

    # get record from given table by given key
    def _get(self, type, key, session=None):
        # check if session is given
        flag = session is None
        if session is None:
            session = self._createSession()

        result = session.query(type).get(key)

        # if session created in def then commit
        if not flag:
            session.commit()

        return result


class UsersDAO(DAO):
    def deleteUserByLogin(self, login):
        session = super()._createSession()
        user = super()._get(User, login, session=session)
        super()._delete(user,session=session)

    def getUserByLogin(self, login):
        user = super()._get(User, login)
        return user

    def getToken(self, token):
        token = super()._get(Token, token)
        return token

    def updatePassword(self, login, newPassword):
        session = super()._createSession()
        user = super()._get(User, login, session=session)
        user.password = newPassword
        session.flush()
        session.commit()

    def addUser(self, user):
        super()._add(user)

    def addToken(self, token):
        super()._add(token)

class WorksDAO(DAO):
    pass
