class PoemPreviewDTO:
    def __init__(self, id, author, title, rating):
        self.id = id
        self.author = author
        self.title = title
        self.rating = rating


class PoemDTO:
    def __init__(self, id, author, title, content, rating, opinions):
        self.id = id
        self.author = author
        self.title = title
        self.content = content
        self.rating = rating
        self.opinions = opinions

    def __str__(self):
        return f'{self.author} : {self.title} : {self.content} : {self.rating} : {self.opinions}'


class OpinionDTO:
    def __init__(self, author, content, rating):
        self.author = author
        self.content = content
        self.rating = rating

    def __str__(self):
        return f'{self.author} : {self.content} : {self.rating}'


class AuthorDTO:
    def __init__(self, name, parsedName, isUserAuthor):
        self.name = name
        self.parsedName = parsedName
        self.isUserAuthor = isUserAuthor

    def __str__(self):
        return f'{self.name} : {self.parsedName} : {self.isUserAuthor}'
