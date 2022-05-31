from services import *
from flask import render_template, request


# app - Flask app object
# registering endpoints from controllers with methods
def registerEndpoints(app):
    app.add_url_rule('/login', view_func=UsersController.login, methods=["POST", "GET"])
    app.add_url_rule('/register', view_func=UsersController.register, methods=["POST", "GET"])


class UsersController:
    __service = UsersService()

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            print(request.form)
            return 'POST LOGIN'

    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            print(request.form)
            return 'POST REGISTER'


class WorksController:
    pass
