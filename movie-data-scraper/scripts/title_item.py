class TitleItem:

    def __init__(self, title='', title_type='', genre='', directors='', actors='', run_time='', release_date='',
                 cover_url=''):
        """
        :param title: String. The title of the movie/tv show.
        :param title_type: String. Options: feature or tv_series.
        :param genre: String. A list of genres the title belongs to.
        :param directors: String. A list of director(s).
        :param actors: String. A list of actor(s).
        :param run_time: String. The runtime of the movie.
        :param release_date: String. The release date of the movie.
        :param cover_url: String. The URL of the media cover.
        """
        self.title = title
        self.title_type = title_type
        self.genre = genre
        self.directors = directors
        self.actors = actors
        self.run_time = run_time
        self.release_date = release_date
        self.cover_url = cover_url
