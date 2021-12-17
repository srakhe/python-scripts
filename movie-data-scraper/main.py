from scripts.scraper import Scraper
from scripts.db import DbHandler

# This is the main script. It is the starting point for execution of all the scripts.

# Global data for the scraper
GENRE = 'horror'
START_YEAR = 2010  # Year to start searching from
END_YEAR = 2019  # Limit year for the search
NUM_TITLES = 100  # Currently only supports 50, 100 or 250 [Limitation by Imdb]

# Global data for the db
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
DB_NAME = 'titles_db'

if __name__ == '__main__':
    scraper_obj = Scraper(genre=GENRE, start_year=START_YEAR, end_year=END_YEAR, num_titles=NUM_TITLES)
    db_obj = DbHandler(host=MONGO_HOST, port=MONGO_PORT, db_name=DB_NAME)

    # Scrape the data and insert it into the db
    list_movies = scraper_obj.scrap_data(title_type='feature')
    done = db_obj.put_data(list_movies, type_title='movies')
    if done:
        print('Movies data was inserted into the db')
    list_shows = scraper_obj.scrap_data(title_type='tv_series')
    done = db_obj.put_data(list_shows, type_title='tv_series')
    if done:
        print('TV shows data was inserted into the db')

    # Get the data from db and print
    count, movies_list_from_db = db_obj.get_data(type_title='movies')
    if movies_list_from_db is not None:
        print(f'Found {count} number of movies in db')
        for movie in movies_list_from_db:
            print(movie)
    count, tv_series_list_from_db = db_obj.get_data(type_title='tv_series')
    if tv_series_list_from_db is not None:
        print(f'Found {count} number of tv series in db')
        for tv_series in tv_series_list_from_db:
            print(tv_series)
