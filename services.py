from DAOs import *
from utils import *
from exceptions import *
from DTOs import *
from datetime import date


class UsersService:
    def __init__(self):
        self.__dao = UsersDAO()

    # check if login is already used
    def isLoginAvailable(self, login):
        user = self.__dao.getUserByLogin(login)
        return user is None

    # create account for new user
    def createNewUser(self, login, password):
        if not self.isLoginAvailable(login):
            raise ValueError("Login jest już zajęty.")

        # prepare password and save user in DB
        salt = generateSalt()
        password = hashPassword(password, salt)
        user = User(login, password, salt)

        # save user in DB
        self.__dao.addUser(user)

        return True

    # login to given account
    def login(self, login, password):
        # check password
        if not self.isPasswordCorrect(login, password):
            raise Unauthorized("Niepoprawny login lub hasło.")

        # generate and save token
        token = generateToken(login)
        tokenObj = Token(token)
        self.__dao.addToken(tokenObj)

        return token

    # in logout delete token from DB
    def logout(self, token):
        self.__dao.deleteToken(token)
        return True

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
        if token is not None:
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
        self.__usersDAO = UsersDAO()

    # add new poem
    def addPoem(self, token, author, title, content, isUserAuthor=False):
        # make validation
        if (author == '' and isUserAuthor is False) or content == '':
            raise ValueError('Wiersz musi posiadać autora i treść.')

        # if title is empty use given pattern: "*** ({first line in poem})"
        if title == '':
            firstLine = content.split('\n')[0]
            title = f"*** ({firstLine})"

        # if user is an author then set his login as author
        if isUserAuthor:
            author = decodeToken(token)[1]

        if self.__poemsDAO.getPoemByAuthorAndTitle(title, author) is not None:
            raise ValueError('Wiersz o takim tytule i autorze już występuje w bazie.')

        poem = Poem(author, title, content.strip(), isUserAuthor)

        try:
            self.__poemsDAO.addPoem(poem)
        except Exception:
            raise InternalServerError('Database error.')

        return True

    # get poem by id
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
            # round to 2 digits
            ratingAvg = int(ratingAvg * 100) / 100

        # create DTO object
        poemDTO = PoemDTO(id, poem.author, poem.title, poem.content.split('\n'), ratingAvg, opinionsDTO)

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

    # return 5 most recent poems for main page view
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
    # parse name and return DTO object of author
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

    # add opinion to poem with id
    def addOpinion(self, id, token, content, rating):
        # TODO: add token validation
        # decode token to get login and User object
        author = decodeToken(token)[1]
        author = self.__usersDAO.getUserByLogin(author)

        rating = int(rating)

        poem = self.__poemsDAO.getPoemById(id)

        # create Opinion object and add to DB
        opinion = createOpinion(content, rating, author, poem)
        self.__opinionsDAO.addOpinion(opinion)

        return True

    # return list of PoemPreviewDTO, where titles contains given title (get first 10 results)
    # using SQL "LIKE %title%"
    def searchPoem(self, title):
        # search poems
        poems = self.__poemsDAO.searchByTitle(title, 10)

        # transfer poems to DTO
        poemsDTO = self._poemsToPoemsPreviewDTO(poems)

        return poemsDTO
