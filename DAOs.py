from sqlalchemy.orm import sessionmaker
from db import *


def mergeSessions(obj1, obj2):
    session1 = DAO.Session.object_session(obj1)
    session2 = DAO.Session.object_session(obj2)

    if session1 is None and session2 is None:
        return
    elif session1 is None:
        session2.add(obj1)
    elif session2 is None:
        session1.add(obj2)
    else:
        session1.expunge(obj1)
        session2.add(obj1)

# base dao class, used for create, delete and get operations
class DAO:
    Session = sessionmaker(bind=engine)

    def _createSession(self):
        session = DAO.Session()
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
        super()._delete(user, session=session)

        # delete user opinions
        opinions = session.query(Opinion).filter(Opinion.author_login == None).delete()

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


class PoemsDAO(DAO):
    def addPoem(self, poem):
        super()._add(poem)

    def getPoemById(self, id):
        return super()._get(Poem, id)

    def getPoemsByAuthor(self, author):
        session = super()._createSession()
        result = session.query(Poem).filter(Poem.author == author, Poem.isUserAuthor == False).all()
        return result

    def getPoemsByUser(self, user):
        session = super()._createSession()
        result = session.query(Poem).filter(Poem.author == user, Poem.isUserAuthor == True).all()
        return result

    def getLastPoems(self, number):
        session = super()._createSession()
        result = session.query(Poem).order_by(-Poem.id).limit(number).all()
        return result


class OpinionsDAO(DAO):
    # get session from opinion's author (user)
    # without that opinion and user/poem are in different sessions
    # TODO: add deleting opinion when user/poem is deleted
    def addOpinion(self, opinion):
        session = DAO.Session.object_session(opinion.user)
        super()._add(opinion, session=session)

    def getPoemOpinions(self, poem):
        session = super()._createSession()
        opinions = session.query(Opinion).filter(Opinion.poem_id == poem.id).all()
        return opinions

