from sqlalchemy import create_engine, Column, String, Integer, Boolean, TEXT, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# storing favourite poems of users
class Favourite(Base):
    __tablename__ = 'favourites'
    __table_args__ = (
        PrimaryKeyConstraint('user_login', 'poem_id'),
    )
    user = Column('user_login', String(255), ForeignKey('users.login'))
    poem = Column('poem_id', Integer, ForeignKey('poems.id'))

    def __init__(self, user, poem):
        self.user = user
        self.poem = poem


# storing users in database
class User(Base):
    __tablename__ = "users"
    __login = Column('login', String(255), primary_key=True)
    __password = Column('password', String(255))
    __salt = Column('salt', String(255))

    opinions = relationship('Opinion', backref='user')
    favourites = relationship('Poem', secondary='favourites', backref='fav_users')

    def __init__(self, login, password, salt):
        self.__login = login
        self.__password = password
        self.__salt = salt

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        self.__login = value

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, value):
        self.__salt = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    def __str__(self):
        return '{' \
               f'login={self.login}; ' \
               f'password={self.password}; ' \
               f'salt={self.salt}' \
               '}'


# storing tokens in database
class Token(Base):
    __tablename__ = "tokens"
    __token = Column('token', String(300), primary_key=True)

    def __init__(self, token):
        self.__token = token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value


class Poem(Base):
    __tablename__ = "poems"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    author = Column('author', String(255))
    title = Column('title', String(255))
    isUserAuthor = Column('is_user_author', Boolean)
    content = Column('content', TEXT)

    opinions = relationship('Opinion', backref='poem')

    def __init__(self, author, title, content, isUserAuthor):
        self.author = author
        self.title = title
        self.isUserAuthor = isUserAuthor
        self.content = content

    def __str__(self):
        return f'{self.id} : {self.author} : {self.title} : {self.isUserAuthor} : {self.content}'


class Opinion(Base):
    __tablename__ = 'opinions'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    content = Column('content', String(1024))
    rating = Column('rating', Integer)
    poem_id = Column(Integer, ForeignKey('poems.id', ondelete='CASCADE'), nullable=False)
    author_login = Column(String(255), ForeignKey('users.login', ondelete='CASCADE'), nullable=False)

    def __init__(self, content, rating, user, poem):
        self.content = content
        self.rating = rating
        self.user = user
        self.poem = poem

    def __str__(self):
        return f'{self.id} : {self.author_login} : {self.poem_id} : {self.rating} : {self.content}'


# creating mysql engine, and connect to DB
engine = create_engine('mysql+pymysql://root:pass@127.0.0.1:3306/daily-poem-db')
Base.metadata.create_all(bind=engine)
