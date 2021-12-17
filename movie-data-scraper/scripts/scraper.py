from scripts.title_item import TitleItem
import requests
from bs4 import BeautifulSoup
import re


class Scraper:

    def __init__(self, genre, start_year, end_year, num_titles):
        self.website_search_url = 'https://www.imdb.com/search/title/'
        self.genre = genre
        self.start_year = start_year
        self.end_year = end_year
        self.num_titles = num_titles
        self.title_items = []

    def scrap_data(self, title_type):
        """Scrapes the data from websites based on the type of title"""
        title_item_list = []
        search_options = {
            'title_type': title_type,
            'sort': 'popularity',
            'release_date': f'{self.start_year},{self.end_year}',
            'genres': str(self.genre),
            'count': str(self.num_titles)
        }
        movies_html = requests.get(self.website_search_url, params=search_options).text
        movies_soup = BeautifulSoup(movies_html, 'html.parser')
        # For the type:
        data_title_type = title_type
        for movie_item in movies_soup.find_all('div', class_='lister-item mode-advanced'):
            data_directors = ''
            data_actors = ''
            # For the title:
            movie_item_header = movie_item.find('h3', class_='lister-item-header')
            data_title = str(movie_item_header.a.text)
            # For the genre:
            data_genre = str(movie_item.find('span', class_='genre').text).strip()
            # For the list of director(s):
            p_text = movie_item.find('p', attrs={'class': ''}).text
            p_text = str(p_text).strip()
            list_dirs_actors = p_text.split('|')
            if len(list_dirs_actors) > 1:
                directors = list_dirs_actors[0].strip()
                actors = list_dirs_actors[1].strip()
                for director in directors.replace('Director:', '').split(','):
                    data_directors += director.replace('\n', '').strip()
                    data_directors += ','
            else:
                actors = list_dirs_actors[0].strip()
            # For the list of actor(s):
            for actor in actors.replace('Stars:', '').split(','):
                data_actors += actor.replace('\n', '').strip()
                data_actors += ','
            # For the run time:
            if movie_item.find('span', class_='runtime') is None:
                data_run_time = ''
            else:
                data_run_time = str(movie_item.find('span', class_='runtime').text)
            # For the release date:
            release_date = movie_item_header.find('span', class_='lister-item-year text-muted unbold').text
            release_date = str(release_date)
            data_release_date = str(re.compile(r'\d+').search(release_date).group())
            # For the cover image URL:
            data_cover_url = str(movie_item.find('img').get('loadlate'))
            title_item_list.append(TitleItem(title=data_title, title_type=data_title_type, genre=data_genre,
                                             directors=data_directors.rstrip(','), actors=data_actors.rstrip(','),
                                             run_time=data_run_time,
                                             release_date=data_release_date, cover_url=data_cover_url))
        return title_item_list
