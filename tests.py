from controllers import *


def testUsersDao():
    dao = UsersDAO()
    newUser = User("testUser1", "testUser1Password", "s")
    newUser1 = User("testUser2", "testUser2Password", "s2")

    dao.addUser(newUser)
    dao.addUser(newUser1)

    print(dao.getUserByLogin('testUser1'))
    print(dao.getUserByLogin('testUser2'))

    dao.updatePassword('testUser1', 'newPassword1')

    print(dao.getUserByLogin('testUser1'))


def testUsersDeleting():
    dao = UsersDAO()
    dao.deleteUserByLogin('testUser1')
    dao.deleteUserByLogin('testUser2')


def testTokens():
    service = UsersService()
    dao = UsersDAO()

    service.createNewUser('testUser', 'testUserPassword')

    token = service.login('testUser', 'testUserPassword')

    print(service.checkToken(token))
    print(service.checkToken("aaaa:asd"))

    dao.deleteUserByLogin('testUser')


def testPoemsDAO():
    dao = PoemsDAO()
    poem = Poem('Konstanty Ildefons Gałczyński', "List jenca", "Kochanie moje, kochanie", False)
    dao.addPoem(poem)


def testAddingPoems():
    service = PoemsService()
    service.addPoem('a', "List jenca", "Kochanie moje, kochanie")
    print(service.getPoem(2))

    try:
        service.addPoem('', "a", "a")
    except ValueError:
        print("value error")

    try:
        service.addPoem('a', "a", "")
    except ValueError:
        print("value error")

def searchingPoems():
    dao = PoemsDAO()

    # poem1 = Poem('Halina Poswiatowska', "a", 'a', False)
    # poem2 = Poem('Halina Poswiatowska', "b", 'b', False)
    # poem3 = Poem('Halina Poswiatowska', "c", 'c', False)
    #
    # dao.addPoem(poem1)
    # dao.addPoem(poem2)
    # dao.addPoem(poem3)

    for x in dao.getPoemsByAuthor('Konstanty Ildefons Gałczyński'):
        print(x)

def getLastPoems():
    dao = PoemsDAO()

    for x in dao.getLastPoems(5):
        print(x)

if __name__ == '__main__':
    # testUsersDao()
    # testUsersDeleting()
    # testTokens()
    # testPoemsDAO()
    # testAddingPoems()
    # searchingPoems()
    getLastPoems()
    pass
