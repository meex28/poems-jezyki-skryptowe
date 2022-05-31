from sqlalchemy import create_engine, Enum, Column, String, Integer, Boolean, TEXT
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as Enumeration

Base = declarative_base()


# storing users in database
class User(Base):
    __tablename__ = "users"
    __login = Column('login', String(255), primary_key=True)
    __password = Column('password', String(255))
    __salt = Column('salt', String(255))

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

    def __init__(self, token, user):
        self.__token = token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value


class WorkType(Enumeration):
    POEM = 1
    PROSE = 2
    DRAMA = 3


# storing works in database
class Work(Base):
    __tablename__ = "works"
    __id = Column('id', Integer, primary_key=True, autoincrement=True)
    __author = Column('author', String(255))
    __title = Column('title', String(255))
    __type = Column('type', Enum(WorkType))
    __isUserAuthor = Column('is_user_author', Boolean)
    __content = Column('content', TEXT)

    def __init__(self, author, title, type, isUserAuthor, content):
        self.__author = author
        self.__title = title
        self.__type = type
        self.__isUserAuthor = isUserAuthor
        self.__content = content

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def isUserAuthor(self):
        return self.__isUserAuthor

    @isUserAuthor.setter
    def isUserAuthor(self, value):
        self.__isUserAuthor = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value


# class Opinion(Base):
#     __tablename__ = 'opinions'
#     __id =

# creating mysql engine, and connect to DB
engine = create_engine('mysql+pymysql://root:pass@127.0.0.1:3306/daily-poem-db')
Base.metadata.create_all(bind=engine)
