from services import *
from flask import render_template, request, make_response, redirect, url_for


# app - Flask app object
# registering endpoints from controllers with methods
def registerEndpoints(app):
    app.add_url_rule('/login', view_func=UsersController.login, methods=["POST", "GET"])
    app.add_url_rule('/register', view_func=UsersController.register, methods=["POST", "GET"])
    app.add_url_rule('/', view_func=PoemsController.mainPage, methods=['GET'])
    app.add_url_rule('/author/<string:author>', view_func=PoemsController.authorPage, methods=['GET'])
    app.add_url_rule('/user/<string:author>', view_func=PoemsController.userAuthorPage, methods=['GET'])
    app.add_url_rule('/poem/<int:id>', view_func=PoemsController.poemPage, methods=['GET', 'POST'])
    app.add_url_rule('/add', view_func=PoemsController.addPoem, methods=['GET', 'POST'])
    app.add_url_rule('/daily', view_func=PoemsController.dailyPoem, methods=['GET'])
    app.add_url_rule('/daily_personal', view_func=PoemsController.dailyPersonalPoem, methods=['GET'])
    app.add_url_rule('/author', view_func=PoemsController.authorsPage, methods=['GET'])


class UsersController:
    __service = UsersService()

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            print(request.form)

            if request.form.get('submit') == 'login':
                user, password = request.form.get('login'), request.form.get('password')
                try:
                    token = UsersController.__service.login(user, password)
                    resp = make_response(redirect(url_for('mainPage')))
                    resp.set_cookie('token', token)
                    return resp
                except Unauthorized as e:
                    return e.message
            elif request.form.get('submit') == 'register':
                return redirect(url_for('register'))

    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            print(request.form)

            if request.form.get('submit') == 'login':
                return redirect(url_for('login'))
            elif request.form.get('submit') == 'register':
                user, password = request.form.get('login'), request.form.get('password')
                UsersController.__service.createNewUser(user, password)
                return redirect(url_for('login'))


class PoemsController:
    __service = PoemsService()

    @staticmethod
    def mainPage():
        poems = PoemsController.__service.getMainPagePoems()
        return render_template('index.html', poems=poems)

    @staticmethod
    def authorPage(author):
        # TODO: add exception handling
        author, poems = PoemsController.__service.getAuthorPoemsPreviews(author)
        return render_template('author_page.html', poems=poems, author=author)

    @staticmethod
    def userAuthorPage(author):
        # TODO: add exception handling
        author, poems = PoemsController.__service.getUserPoemsPreviews(author)
        return render_template('author_page.html', poems=poems, author=author)

    @staticmethod
    def poemPage(id):
        if request.method == 'GET':
            poem = PoemsController.__service.getPoem(id)
            return render_template('poem_page.html', poem=poem)
        elif request.method == 'POST':
            if request.cookies.get('token') is None:
                return redirect(url_for('login'))

            PoemsController.__service.addOpinion(id, request.cookies.get('token'),
                                                 request.form.get('content'), request.form.get('rating'))
            poem = PoemsController.__service.getPoem(id)

            return render_template('poem_page.html', poem=poem)

    @staticmethod
    def addPoem():
        if request.method == 'GET':
            return render_template('add_poem_page.html')
        elif request.method == 'POST':
            author = request.form.get('author')
            isUserAuthor = request.form.get('isUserAuthor') == 'on'
            title = request.form.get('title')
            content = request.form.get('content')
            PoemsController.__service.addPoem(author, title, content, isUserAuthor)

            # TODO: add message of result
            return redirect(url_for('addPoem'))

    @staticmethod
    def dailyPoem():
        poem = PoemsController.__service.getDailyPoem()
        return render_template('poem_page.html', poem=poem)

    @staticmethod
    def dailyPersonalPoem():
        token = request.cookies.get('token')
        poem = PoemsController.__service.getDailyPoem(token=token)
        return render_template('poem_page.html', poem=poem)

    @staticmethod
    def authorsPage():
        authors = PoemsController.__service.getAuthors()
        return render_template('authors.html', authors=authors)
