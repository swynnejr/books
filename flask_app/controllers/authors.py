from flask_app import app
from flask import render_template, redirect, session, request
# from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route('/authors')
def display_authors():
    authors = Author.get_all_authors()
    return render_template('authors.html', authors = authors)

@app.route('/authors/create', methods=['POST'])
def create_author():

    if Author.validate_author(request.form):
        data = {
            'name': request.form['name'],
        }
        Author.create_author(data)
        print('author valid')
        return redirect('/authors')
    print('author invalid')
    return redirect('/authors')
