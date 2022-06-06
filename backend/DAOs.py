from sqlalchemy.orm import sessionmaker
from backend.db import engine, User, Poem, Opinion, Token, Favourite


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


def createOpinion(content, rating, author, poem):
    mergeSessions(author, poem)
    return Opinion(content, rating, author, poem)

# base dao class, used for create, delete and get operations
class DAO:
    current_session = None
    Session = sessionmaker(bind=engine)

    def _createSession(self):
        if DAO.current_session is None:
            DAO.current_session = DAO.Session()

        # session = DAO.Session()
        return DAO.current_session

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
    # delete user with given login
    def deleteUserByLogin(self, login):
        session = super()._createSession()
        user = super()._get(User, login, session=session)
        super()._delete(user, session=session)

        # delete user opinions
        opinions = session.query(Opinion).filter(Opinion.author_login == None).delete()

    # get User object with given login
    def getUserByLogin(self, login):
        user = super()._get(User, login)
        return user

    # get Token object
    def getToken(self, token):
        token = super()._get(Token, token)
        return token

    # update password for given User
    def updatePassword(self, login, newPassword):
        session = super()._createSession()
        user = super()._get(User, login, session=session)
        user.password = newPassword
        session.flush()
        session.commit()

    # add new User
    def addUser(self, user):
        super()._add(user)

    # add new Token
    def addToken(self, token):
        super()._add(token)

    # delete Token
    def deleteToken(self, token):
        session = super()._createSession()
        token = super()._get(Token, token, session=session)
        if token is not None:
            super()._delete(token, session=session)


class PoemsDAO(DAO):
    # add new Poem
    def addPoem(self, poem):
        super()._add(poem)

    # get one poem by id
    def getPoemById(self, id):
        return super()._get(Poem, id)

    # get list of poems by given id
    def getPoemsByIds(self, idList):
        res = []
        for idd in idList:
            res.append(self.getPoemById(idd))
        return res

    # get poems of given author
    def getPoemsByAuthor(self, author):
        session = super()._createSession()
        result = session.query(Poem).filter(Poem.author == author, Poem.isUserAuthor == False).all()
        return result

    # get poems of given user
    def getPoemsByUser(self, user):
        session = super()._createSession()
        result = session.query(Poem).filter(Poem.author == user, Poem.isUserAuthor == True).all()
        return result

    # get most recent poem
    def getLastPoems(self, number):
        session = super()._createSession()
        result = session.query(Poem).order_by(-Poem.id).limit(number).all()
        return result

    # count number of poems in DB
    def countPoems(self):
        session = super()._createSession()
        number = session.query(Poem).count()
        return number

    # get ID of nth row in table
    # index from 0
    def getNthPoem(self, number):
        session = super()._createSession()
        result = session.query(Poem).limit(number+1).all()
        return result[len(result)-1]

    # get list of authors
    def getAuthors(self):
        session = super()._createSession()
        authors = [(poem.author, poem.isUserAuthor) for poem in session.query(Poem).group_by(Poem.author).all()]
        return authors

    # search poems by title, using SQL "LIKE %title%"
    # limited to {limit} first results
    def searchByTitle(self, title, limit):
        session = super()._createSession()
        poems = session.query(Poem).filter(Poem.title.like(f'%{title}%')).limit(limit).all()
        return poems

    # get Poem with given author and title
    def getPoemByAuthorAndTitle(self, title, author):
        session = super()._createSession()
        poem = session.query(Poem).filter(Poem.title == title, Poem.author == author).first()
        return poem


class OpinionsDAO(DAO):
    # get session from opinion's author (user)
    # without that opinion and user/poem are in different sessions
    def addOpinion(self, opinion):
        session = DAO.Session.object_session(opinion.user)
        super()._add(opinion, session=session)

    # get opinions for given poem
    def getPoemOpinions(self, poem):
        session = super()._createSession()
        opinions = session.query(Opinion).filter(Opinion.poem == poem).all()
        return opinions

    # add poem to user's favourites
    def addToFavourites(self, login, poemId):
        fav = Favourite(login, poemId)
        super()._add(fav)

    # delete poem from user's favourites
    def deleteFromFavourites(self, login, poemId):
        fav = self.getFavouriteObject(login, poemId)
        if fav is not None:
            super()._delete(fav, session=DAO.Session.object_session(fav))

    # return list of poems IDs
    def getFavouritesOfUser(self, login):
        session = super()._createSession()
        favs = session.query(Favourite).filter(Favourite.user == login).all()
        poems = [fav.poem for fav in favs]
        return poems

    # get object of login and poemId favourite
    def getFavouriteObject(self, login, poemId):
        session = super()._createSession()
        res = session.query(Favourite).filter(Favourite.user == login, Favourite.poem == poemId).first()
        return res