import json
from fastapi import FastAPI
from typing import List

from backend.Models.Data_models import Director_Movies

from backend.app.utilities import connect_postgres, connect_redis, fix_genres

app = FastAPI()


def fetch_directors_movies(director_name: str) -> List[Director_Movies]:

    # check redis first
    try:
        r = connect_redis()

        cached_data = r.get(director_name)
        if cached_data:
            # Return cached data
            return json.loads(cached_data)
    except Exception as e:
        print(f"Could not connect to redis : {e}")
        r = None

    try:
        # Very inefficent sql query to test it out
        conn = connect_postgres()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT \
                a.title, \
                b.startYear, \
                b.genres, \
                r.averageRating, \
                n.primaryName AS director \
                FROM title_akas a \
            JOIN title_basics b ON a.titleId = b.tconst \
            JOIN title_ratings r ON b.tconst = r.tconst \
            JOIN title_crew c ON b.tconst = c.tconst \
            JOIN name_basics n ON n.nconst = ANY(c.directors) \
            WHERE n.primaryName ILIKE (%s) \
            ORDER BY r.averageRating DESC;",
            (director_name,),
        )
        results = cursor.fetchmany(10)
        cursor.close()
        conn.close()

        # fetch* returns a list of tuples
        response_dict_list = []
        for result in results:
            temp_dict = {
                "title": result[0],
                "year": result[1],
                "genres": fix_genres(
                    result[2]
                ),  # genres are stored incrroectly.
                "imdbRating": float(result[3]),
                "director": result[4],
            }
            response_dict_list.append(temp_dict)

        # Cache the data in Redis with a 10-day expiration, if redis is connected
        if r:
            r.set(director_name, json.dumps(response_dict_list), ex=2592000)

    except Exception as e:
        print(f"Could not connect to postgres : {e}")

        # Test error response
        response_dict_list = [
            {
                "title": "Dummy",
                "year": 2010,
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "imdbRating": 8.8,
                "director": "Christopher Nolan",
            }
        ]

    return response_dict_list


@app.get("/search_director/{director_name}")
async def search_director(director_name: str):

    director_movie_data = fetch_directors_movies(director_name)

    return director_movie_data
