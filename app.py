# from helper import search_books, filter_list
from book_recommender import find_k_similar_books, book_lookup, get_top_books
from flask import Flask, render_template, request, jsonify, Response
import json

# virtualenv book_search
# source book_search/bin/activate
# export FLASK_APP=app.py
# export FLASK_ENV=development
# flask run

# Heroku
# https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/
# https://devcenter.heroku.com/articles/dynos

app = Flask(__name__)

# https://blog.miguelgrinberg.com/post/using-celery-with-flask
# from celery import Celery

# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# correlation_matrix = None

# @celery.task
# def load_book_recommender():
#     from book_recommender import calculate_correlation_matrix

#     correlation_matrix = calculate_correlation_matrix()
#     return {"status": True}

# @app.before_first_request
# def activate_job():
#     # load_book_recommender.delay()
#     global correlation_matrix
#     correlation_matrix = calculate_correlation_matrix()

@app.route('/')
def index():
    # app.logger.debug('started')
    # books = get_top_books(n=20)
    return render_template('index.html')

@app.route('/search_book', methods=['GET'])
def search_book():
    # Get parameter from the URL
    search_string = request.args.get('search_field')

    # books = search_books(search)
    # filtered_books = filter_list(books, ['isbn','cover_i','title','id_goodreads'])

    filtered_books = book_lookup(search_string, n=20)
    return render_template('index.html', books=filtered_books)

@app.route('/book_recommendations/<id_goodreads>')
def book_recommendations(id_goodreads):
    # id_goodreads = request.args.get('id_goodreads')
    recommended_books = find_k_similar_books(goodreads_book_id=id_goodreads, n=20)
    return render_template('index.html', books=recommended_books)


if __name__ == '__main__':
    app.run()