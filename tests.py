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

if __name__ == '__main__':
    # testUsersDao()
    # testUsersDeleting()
    testTokens()
    pass