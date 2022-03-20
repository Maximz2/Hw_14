import sqlite3

from flask import Flask, jsonify, request

from functions import search_most_recent_movie_by_name, search_by_two_years, search_by_rating, search_by_genre

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def page_movie_title(title):
    film = search_most_recent_movie_by_name(title)
    return jsonify(film)


@app.route('/movie/year/to/year/')
def page_movie_years():
    years = request.args.getlist('year')
    films = search_by_two_years(years[0], years[1])
    return jsonify(films)


@app.route('/rating/<rating>')
def page_movie_rating(rating):
    try:
        films = search_by_rating(rating)
        return jsonify(films)
    except sqlite3.OperationalError:
        return "Нет такой категории рейтинга"


@app.route('/genre/<genre>')
def page_movie_genre(genre):
    try:
        films = search_by_genre(genre)
        return jsonify(films)
    except AttributeError:
        return False


if __name__ == '__main__':
    app.run()
