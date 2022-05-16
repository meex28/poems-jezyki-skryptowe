from flask import Flask, render_template, request
from Users import UsersController

app = Flask(__name__)
app.add_url_rule('/login', view_func=UsersController.login, methods=["POST", "GET"])
app.add_url_rule('/register', view_func=UsersController.register, methods=["POST", "GET"])

if __name__ == '__main__':
    app.run()
