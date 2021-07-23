from flask_app import app
from flask import render_template, redirect, session, request
# from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.book import Book

@app.route('/books')
def display_books():
    books = Book.get_all_books()
    return render_template('books.html', books = books)

@app.route('/books/create', methods=['POST'])
def create_book():

    if Book.validate_book(request.form):
        data = {
            'title': request.form['title'],
            'num_of_pages': request.form['num_of_pages']
        }
        Book.create_book(data)
        print('book valid')
        return redirect('/books')
    print('book invalid')
    return redirect('/books')