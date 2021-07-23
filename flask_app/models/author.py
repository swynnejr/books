from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book
from flask import flash

class Author():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.book_id = data['book_id']
        self.user = None

    @classmethod
    def create_author(cls, data):

        query = 'INSERT INTO authors (name) VALUES (%(name)s);'

        result = connectToMySQL('books_schema').query_db(query, data)

        return result

    @staticmethod
    def validate_author(data):

        is_valid = True

        if len(data['name']) < 1 or len(data['name']) > 100:
            flash("Author name should be 1 to 100 characters.")
            is_valid = False

        return is_valid

    @classmethod
    def get_all_authors(cls):
# This is the literal query being run in MySQL, you can and should test them in MySQL if they are complicated
        query = "SELECT * FROM authors;"

        results = connectToMySQL('books_schema').query_db(query)

        authors = []

        for item in results:
# You can use cls OR the name of the actual class above
            authors.append(Author(item))

        return authors


    @classmethod
    def get_all_authors_favorites(cls):

        query = 'SELECT * FROM authors JOIN favorites ON authors.id = favorites.book_id;'

        results = connectToMySQL('books_schema').query_db(query)

        authors = []

        for item in results:
            author = cls(item)
            author_data = {
                'id': item['authors.id'],
                'name': item['authors.name'],
                'created_at': item['authors.created_at'],
                'updated_at': item['authors.updated_at'],
                'book_id': item['favorites.book_id']
            }
            author.book = Book(author_data)
            authors.append(author)

        return authors

