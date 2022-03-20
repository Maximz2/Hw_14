import sqlite3


def query_db_by_title(title):
    """Запрос в БД последнего фильма, по наименованию"""
    search = (f'%{title}%',)
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = """
                       SELECT title, country, release_year, listed_in, description
                       FROM netflix
                       WHERE type = 'Movie' AND title LIKE ?
                       ORDER BY release_year DESC
                       LIMIT 1
        """
        cur.execute(sqlite_query, search)
        result = cur.fetchone()
        print(search)
    return result


def query_db_by_release_year(year_start, year_end):
    """Запрос в БД фильмов по диапазону лет выпуска"""
    search = (str(year_start), str(year_end))
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = """
                       SELECT title, release_year
                       FROM netflix
                       WHERE type = 'Movie' AND release_year BETWEEN ? AND ?
                       ORDER BY duration DESC
                       LIMIT 100
                       """
        cur.execute(sqlite_query, search)
        result = cur.fetchall()
    return result


def query_db_by_rating(rating_group):
    """Запрос в БД фильмов по списку рейтингов"""
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = f"""
                       SELECT rating, title, description
                       FROM netflix
                       WHERE rating IN {rating_group}
                       """
        cur.execute(sqlite_query)
        result = cur.fetchall()
    return result


def query_db_by_genre(genre):
    """Запрос в БД 10 последних фильмов по жанру"""
    search = (f'%{genre}%',)
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = """
                       SELECT title, description
                       FROM netflix
                       WHERE listed_in LIKE ?
                       ORDER BY release_year DESC
                       LIMIT 10
                       """
        cur.execute(sqlite_query, search)
        result = cur.fetchall()
    return result


def query_db_by_actors(actor1, actor2):
    """Запрос в БД актеров, сыгравших с двумя заданными актерами в одном фильме два и более раза"""
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = f"""
                       SELECT "cast"
                       FROM netflix
                       WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
                       """
        cur.execute(sqlite_query)
        result = cur.fetchall()
    return result


def query_db_by_type_year_genre(type_movie, year, genre):
    """Запрос в БД фильмов по типу, году и жанру"""
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sqlite_query = f"""
                       SELECT *
                       FROM netflix
                       WHERE "type" = '{type_movie}' 
                       AND release_year = '{year}' 
                       AND listed_in LIKE '%{genre}%'                       
                       """
        cur.execute(sqlite_query)
        result = cur.fetchall()
        return result
