from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    login = Column('login', String(255), primary_key=True)
    password = Column('password', String(255))
    salt = Column('salt', String(255))

    def __init__(self, login, password, salt):
        self.login = login
        self.password = password
        self.salt = salt

    def __str__(self):
        return '{' \
               f'login={self.login}; ' \
               f'password={self.password}; ' \
               f'salt={self.salt}' \
               '}'


class Token(Base):
    __tablename__ = "tokens"
    token = Column('token', String(300), primary_key=True)

    def __init__(self, token, user):
        self.token = token


engine = create_engine('mysql+pymysql://root:pass@127.0.0.1:3306/daily-poem-db')
Base.metadata.create_all(bind=engine)
