from services import *
from flask import render_template, request, make_response, redirect, url_for


# app - Flask app object
# registering endpoints from controllers with methods
def registerEndpoints(app):
    app.add_url_rule('/login', view_func=UsersController.login, methods=["POST", "GET"])
    app.add_url_rule('/logout', view_func=UsersController.logout, methods=["GET"])
    app.add_url_rule('/register', view_func=UsersController.register, methods=["POST", "GET"])
    app.add_url_rule('/', view_func=PoemsController.mainPage, methods=['GET'])
    app.add_url_rule('/author/<string:author>', view_func=PoemsController.authorPage, methods=['GET'])
    app.add_url_rule('/user/<string:author>', view_func=PoemsController.userAuthorPage, methods=['GET'])
    app.add_url_rule('/poem/<int:id>', view_func=PoemsController.poemPage, methods=['GET', 'POST'])
    app.add_url_rule('/add', view_func=PoemsController.addPoem, methods=['GET', 'POST'])
    app.add_url_rule('/daily', view_func=PoemsController.dailyPoem, methods=['GET'])
    app.add_url_rule('/daily_personal', view_func=PoemsController.dailyPersonalPoem, methods=['GET'])
    app.add_url_rule('/author', view_func=PoemsController.authorsPage, methods=['GET'])
    app.add_url_rule('/poem/<int:id>/opinion', view_func=PoemsController.addOpinion, methods=['GET', 'POST'])
    app.add_url_rule('/search', view_func=PoemsController.searchPoems, methods=['GET', 'POST'])
    app.add_url_rule('/fav/add/<int:id>', view_func=PoemsController.addToFavourites, methods=['GET'])
    app.add_url_rule('/fav/remove/<int:id>', view_func=PoemsController.removeFromFavourites, methods=['GET'])
    app.add_url_rule('/fav', view_func=PoemsController.favouritePoems, methods=['GET'])


class UsersController:
    __service = UsersService()

    @staticmethod
    def checkToken(r):
        token = r.cookies.get('token')
        return UsersController.__service.checkToken(token)[0]

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template('login.html', logged=UsersController.checkToken(request))
        elif request.method == 'POST':
            if request.form.get('submit') == 'login':
                user, password = request.form.get('login'), request.form.get('password')
                try:
                    token = UsersController.__service.login(user, password)
                    resp = make_response(redirect(url_for('mainPage', logged=UsersController.checkToken(request))))
                    resp.set_cookie('token', token)
                    return resp
                except Unauthorized as e:
                    return UsersController.error(str(e), request)
            elif request.form.get('submit') == 'register':
                return redirect(url_for('register', logged=UsersController.checkToken(request)))

    @staticmethod
    def logout():
        if request.method == 'GET':
            token = request.cookies.get('token')
            if token is None:
                return redirect(url_for('login', logged=UsersController.checkToken(request)))

            UsersController.__service.logout(token)
            resp = make_response(redirect(url_for('mainPage', logged=False)))
            resp.delete_cookie('token')
            return resp

    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template('register.html', logged=UsersController.checkToken(request))
        elif request.method == 'POST':
            if request.form.get('submit') == 'login':
                return redirect(url_for('login', logged=UsersController.checkToken(request)))
            elif request.form.get('submit') == 'register':
                user, password = request.form.get('login'), request.form.get('password')
                try:
                    UsersController.__service.createNewUser(user, password)
                except ValueError as e:
                    return UsersController.error(str(e), request)

                return redirect(url_for('login', logged=UsersController.checkToken(request)))

    @staticmethod
    def error(message, r):
        return render_template('error.html', message=message, logged=UsersController.checkToken(r))


class PoemsController:
    __service = PoemsService()

    @staticmethod
    def mainPage():
        poems = PoemsController.__service.getMainPagePoems()
        return render_template('index.html', poems=poems, logged=UsersController.checkToken(request))

    @staticmethod
    def authorPage(author):
        # TODO: add exception handling
        author, poems = PoemsController.__service.getAuthorPoemsPreviews(author)
        return render_template('author_page.html', poems=poems, author=author,
                               logged=UsersController.checkToken(request))

    @staticmethod
    def userAuthorPage(author):
        # TODO: add exception handling
        author, poems = PoemsController.__service.getUserPoemsPreviews(author)
        return render_template('author_page.html', poems=poems, author=author,
                               logged=UsersController.checkToken(request))

    @staticmethod
    def poemPage(id):
        if request.method == 'GET':
            poem = PoemsController.__service.getPoem(id)
            token = request.cookies.get('token')
            isFav = PoemsController.__service.isFavourite(token, id)
            return render_template('poem_page.html', poem=poem, logged=UsersController.checkToken(request), isFav=isFav)

    @staticmethod
    def addOpinion(id):
        if request.method == 'GET':
            return render_template('add_opinion_page.html', id=id, logged=UsersController.checkToken(request))
        elif request.method == 'POST':
            if request.cookies.get('token') is None:
                return redirect(url_for('login', logged=UsersController.checkToken(request)))

            PoemsController.__service.addOpinion(id, request.cookies.get('token'),
                                                 request.form.get('content'), request.form.get('rating'))
            poem = PoemsController.__service.getPoem(id)

            return render_template('poem_page.html', poem=poem, logged=UsersController.checkToken(request))

    @staticmethod
    def addPoem():
        if request.method == 'GET':
            if not UsersController.checkToken(request):
                return redirect(url_for('login', logged=UsersController.checkToken(request)))
            return render_template('add_poem_page.html', logged=UsersController.checkToken(request))
        elif request.method == 'POST':
            if not UsersController.checkToken(request):
                return redirect(url_for('login', logged=UsersController.checkToken(request)))
            author = request.form.get('author')
            isUserAuthor = request.form.get('isUserAuthor') == 'on'
            title = request.form.get('title')
            content = request.form.get('content')
            try:
                PoemsController.__service.addPoem(request.cookies.get('token'), author, title, content, isUserAuthor)
            except ValueError as e:
                return UsersController.error(str(e), request)

            return redirect(url_for('addPoem', logged=UsersController.checkToken(request)))

    @staticmethod
    def dailyPoem():
        poem = PoemsController.__service.getDailyPoem()
        return render_template('poem_page.html', poem=poem, logged=UsersController.checkToken(request))

    @staticmethod
    def dailyPersonalPoem():
        token = request.cookies.get('token')

        if token is None:
            return redirect(url_for('login'))

        poem = PoemsController.__service.getDailyPoem(token=token)
        return render_template('poem_page.html', poem=poem, logged=UsersController.checkToken(request))

    @staticmethod
    def authorsPage():
        authors = PoemsController.__service.getAuthors()
        return render_template('authors.html', authors=authors, logged=UsersController.checkToken(request))

    @staticmethod
    def searchPoems():
        title = ''
        if request.method == 'GET':
            title = ''
        elif request.method == 'POST':
            title = request.form.get('title')
        poems = PoemsController.__service.searchPoem(title)
        return render_template('searching_page.html', poems=poems, logged=UsersController.checkToken(request))

    @staticmethod
    def addToFavourites(id):
        token = request.cookies.get('token')

        if token is None:
            return redirect(url_for('login'))

        PoemsController.__service.addToFavourites(token, id)
        return redirect(url_for('poemPage', id=id))

    @staticmethod
    def removeFromFavourites(id):
        token = request.cookies.get('token')

        if token is None:
            return redirect(url_for('login'))

        PoemsController.__service.removeFromFavourites(token, id)
        return redirect(url_for('poemPage', id=id))

    @staticmethod
    def favouritePoems():
        token = request.cookies.get('token')

        if token is None:
            return redirect(url_for('login'))

        poems = PoemsController.__service.getFavouritePoems(token)
        return render_template('favourite_poems.html', poems=poems, logged=UsersController.checkToken(request))