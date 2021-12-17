from scripts.title_item import TitleItem
from pymongo import MongoClient


class DbHandler:

    def __init__(self, host, port, db_name):
        self.mongo_host = host
        self.mongo_port = port
        self.admin_mongo_client = MongoClient(f'{self.mongo_host}:{self.mongo_port}')
        self.db_name = db_name

    def init_db(self):
        """Initializes the database and returns the control to that database (Cursor)."""
        if self.db_name in self.admin_mongo_client.list_database_names():
            return self.admin_mongo_client[self.db_name]
        titles_db = self.admin_mongo_client[self.db_name]
        init_col = titles_db['init_col']
        init_col.insert_one({'init': 'This is to init the db!'})
        return self.admin_mongo_client[self.db_name]

    def put_data(self, list_titles, type_title):
        """Inserts each title object into the database depending on the type of the title."""
        get_db = self.init_db()
        if type_title == 'movies':
            collection = get_db['movies']
        elif type_title == 'tv_series':
            collection = get_db['tv_series']
        else:
            return False
        title: TitleItem
        for title in list_titles:
            title_document = {
                'title': title.title,
                'title_type': title.title_type,
                'genre': title.genre,
                'directors': title.directors,
                'actors': title.actors,
                'run_time': title.run_time,
                'release_date': title.release_date,
                'cover_url': title.cover_url
            }
            collection.insert_one(title_document)
        return True

    def get_data(self, type_title):
        """Returns the count of rows and the data from the collection in the database depending on type of the title."""
        get_db = self.init_db()
        if type_title == 'movies':
            collection = get_db['movies']
        elif type_title == 'tv_series':
            collection = get_db['tv_series']
        else:
            return
        reply = collection.find({})
        return reply.count(), list(reply)
