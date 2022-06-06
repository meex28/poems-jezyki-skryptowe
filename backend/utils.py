import secrets
import string
import hmac
import hashlib
import base64


def generateRandomString(length):
    alphabet = string.ascii_letters + string.digits
    res = ''.join(secrets.choice(alphabet) for i in range(length))
    return res


# decoding token, on return tuple with decoded token and login
def decodeToken(token):
    token = token.encode()
    token = base64.b64decode(token).decode()
    return tuple(token.split(':'))


# generate token in format {random string of 32 length}:{login}
def generateToken(login):
    token = f'{generateRandomString(32)}:{login}'.encode()
    token = base64.b64encode(token).decode()
    return token


def generateSalt():
    return generateRandomString(8)


def hashPassword(password, salt):
    password = password.encode()
    salt = salt.encode()

    return hmac.new(password, salt, hashlib.sha256).hexdigest()


def countAsciiSum(s):
    return sum(map(ord, s))
