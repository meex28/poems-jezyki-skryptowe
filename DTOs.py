class PoemPreviewDTO:
    def __init__(self, href, author, title, rating):
        self.href = href
        self.author = author
        self.title = title
        self.rating = rating


class PoemDTO:
    def __init__(self, author, title, content, rating, reviews):
        self.author = author
        self.title = title
        self.content = content
        self.rating = rating
        self.reviews = reviews

    def __str__(self):
        return f'{self.author} : {self.title} : {self.content} : {self.rating} : {self.reviews}'
