from flask import json

from sql_func import query_db_by_title, query_db_by_release_year, query_db_by_rating, query_db_by_genre, \
    query_db_by_actors, query_db_by_type_year_genre
from settings import rating_dict


def search_most_recent_movie_by_name(title):
    """Поиск последнего фильма, по наименованию"""
    result_tuple = query_db_by_title(title)
    result = {
        "title": result_tuple[0],
        "country": result_tuple[1],
        "release_year": result_tuple[2],
        "genre": result_tuple[3],
        "description": result_tuple[4],
    }
    return result


def search_by_year(year):
    """Поиск фильмов по году"""
    result_list = query_db_by_release_year(year, year)
    result = []
    for movie in result_list:
        result.append({
            "title": movie[0],
            "release_year": movie[1],
        })
    return result


def search_by_two_years(year1, year2):
    """Поиск фильмов по двум годам"""
    result = search_by_year(year1) + search_by_year(year2)
    return result


def search_by_rating(rating):
    """Поиск фильмов по рейтингу"""
    result_list = query_db_by_rating(rating_dict.get(rating))
    result = []
    for movie in result_list:
        result.append({
            "rating": movie[0],
            "title": movie[1],
            "description": movie[2],
        })
    return result


def search_by_genre(genre):
    """Поиск фильмов по жанру"""
    result_list = query_db_by_genre(genre)
    result = []
    for movie in result_list:
        result.append({
            "title": movie[0],
            "description": movie[1],
        })
    return result


def search_actors(actor1, actor2):
    """Поиск актеров"""
    actors_list = query_db_by_actors(actor1, actor2)
    actors_name = []
    for actors_tuple in actors_list:
        for actors in actors_tuple:
            actors_movie = actors.split(', ')
            for actor in actors_movie:
                actors_name.append(actor)
    actors_name_check = set(actors_name) - {actor1, actor2}
    result = []
    for actor_name in actors_name_check:
        count = 0
        for actor in actors_name:
            if actor_name == actor:
                count += 1
            else:
                continue
            if count > 2:
                result.append(actor_name)
    return result


def search_by_type_year_genre(type_movie, release_year, genre):
    """Поиск по типу картины (фильм или сериал), году выпуска и ее жанру"""
    response = query_db_by_type_year_genre(type_movie, release_year, genre)
    result = []
    for i in response:
        result.append(dict(i))
    return json.dumps(result, indent=4)


# print(search_actors('Jack Black', 'Dustin Hoffman'))
# print(search_by_type_year_genre('TV Show', '2020', 'Dramas'))
