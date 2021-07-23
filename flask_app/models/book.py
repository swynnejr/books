from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.author import Author
from flask import flash

class Book():

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.author_id = data['author_id']
        self.user = None

    @classmethod
    def create_book(cls, data):

        query = 'INSERT INTO books (title, num_of_pages) VALUES (%(title)s), %(num_of_pages)s);'

        result = connectToMySQL('books_schema').query_db(query, data)

        return result

    @staticmethod
    def validate_book(data):

        is_valid = True

        if len(data['title']) < 1 or len(data['title']) > 100:
            flash("book name should be 1 to 100 characters.")
            is_valid = False

        if len(data['num_of_pages']) < 1:
            flash("Books should have pages.")
            is_valid = False

        return is_valid

    @classmethod
    def get_all_books(cls):
# This is the literal query being run in MySQL, you can and should test them in MySQL if they are complicated
        query = "SELECT * FROM books;"

        results = connectToMySQL('books_schema').query_db(query)

        books = []

        for item in results:
# You can use cls OR the name of the actual class above
            books.append(Book(item))

        return books


    @classmethod
    def get_all_books_favorites(cls):

        query = 'SELECT * FROM books JOIN favorites ON books.id = favorites.book_id;'

        results = connectToMySQL('books_schema').query_db(query)

        books = []

        for item in results:
            book = cls(item)
            book_data = {
                'id': item['books.id'],
                'name': item['books.name'],
                'created_at': item['books.created_at'],
                'updated_at': item['books.updated_at'],
                'book_id': item['favorites.book_id']
            }
            book.book = Book(book_data)
            books.append(book)

        return books
