from DAOs import *
from utils import *
from exceptions import *
from DTOs import *
from random import randint
from datetime import date

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


class PoemsService:
    def __init__(self):
        self.__poemsDAO = PoemsDAO()
        self.__opinionsDAO = OpinionsDAO()

    def addPoem(self, author, title, content, isUserAuthor=False):
        if author == '' or content == '':
            raise ValueError('Wiersz musi posiadac autora i tresc!')

        if title == '':
            firstLine = content.split('\n')[0]
            title = f"*** ({firstLine})"

        poem = Poem(author, title, content, isUserAuthor)

        try:
            self.__poemsDAO.addPoem(poem)
        except:
            raise InternalServerError('Database error.')

        return True

    def getPoem(self, id):
        poem = self.__poemsDAO.getPoemById(id)
        opinions = self.__opinionsDAO.getPoemOpinions(poem)
        # make opinions DTO objects from poem (drop poem_id, id)
        opinionsDTO = [OpinionDTO(opinion.author_login, opinion.content, opinion.rating) for opinion in opinions]

        # count average rating on poem opinions
        ratingAvg = 0
        for opinion in opinionsDTO:
            ratingAvg += opinion.rating
        if len(opinionsDTO) != 0:
            ratingAvg /= len(opinionsDTO)

        poemDTO = PoemDTO(poem.author, poem.title, poem.content, ratingAvg, opinionsDTO)

        return poemDTO

    # create DTO objects to preview poems (contains id, author, title) from poem objects
    def _poemsToPoemsPreviewDTO(self, poems):
        poemsDTO = [PoemPreviewDTO(poem.id, poem.author, poem.title, None) for poem in poems]
        return poemsDTO

    # get username
    # return username and his poems
    def getUserPoemsPreviews(self, author):
        poems = self.__poemsDAO.getPoemsByUser(author)

        # check if given author exist in DB
        if len(poems) == 0:
            raise ValueError('Brak podanego autora w bazie!')

        return author, self._poemsToPoemsPreviewDTO(poems)

    # get author name in format with _ instead of whitespaces
    # return parsed author name and his poems
    def getAuthorPoemsPreviews(self, author):
        # parse author name
        author = author.replace('_', ' ')

        poems = self.__poemsDAO.getPoemsByAuthor(author)

        # check if given author exist in DB
        if len(poems) == 0:
            raise ValueError('Brak podanego autora w bazie!')

        return author, self._poemsToPoemsPreviewDTO(poems)

    def getMainPagePoems(self):
        poems = self.__poemsDAO.getLastPoems(5)
        # TODO: pass opinions in constructor

        return self._poemsToPoemsPreviewDTO(poems)

    def getDailyPoem(self, token=None):
        numberOfPoems = self.__poemsDAO.countPoems()
        today = date.today()

        poemNumber = countAsciiSum(str(today))

        if token is not None:
            login = decodeToken(token)[1]
            poemNumber += countAsciiSum(str(login))

        poemNumber %= numberOfPoems
        poemId = self.__poemsDAO.getNthPoem(poemNumber).id

        return self.getPoem(poemId)

    # get tupple of (authorName, isUserAuthor)

    def __authorsToDTO(self, poem):
        result = AuthorDTO(poem[0], poem[0], poem[1])

        if not poem[1]:
            result.parsedName = poem[0].replace(' ', '_')
        return result

    # get list of authors
    def getAuthors(self):
        authors = self.__poemsDAO.getAuthors()

        # check if author is user of service and parse name
        authors = list(map(self.__authorsToDTO, authors))

        return authors
