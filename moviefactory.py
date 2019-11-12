import dbfactory
from movie import Movie

class MovieFactory(dbfactory.DbFactory):

    # def __init__(self):
        # connection à la base ? 


    def insert(self,movie):
        cnx = self.db_connect()
        cursor = self.create_cursor()
        add_movie = ("INSERT INTO movies "
               "(title, original_title, synopsis, duration, production_budget, release_date, vote_average, revenue, tmdb_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_movie = (movie.title, movie.original_title, movie.synopsis, movie.duration, movie.production_budget, movie.release_date, movie.vote_average, movie.revenue, movie.tmdb_id)
        cursor.execute(add_movie, data_movie)
        movie.id = cursor.lastrowid
        cnx.commit()
        self.close_cursor()
        self.db_disconnect

    # Check if film is already in database with his tmdb_id 
    # Pourrait retourner un objet movie ? 
    def find_by_tmdb_id(self,id):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT * FROM movies where tmdb_id = {}".format(id))
        cursor.execute(query)
        results = cursor.fetchall()
        movie = None
        if cursor.rowcount == 1:
            row = results[0]
            movie = Movie(row['title'], row['original_title'], row['synopsis'], row['duration'], row['production_budget'], row['release_date'], row['vote_average'], row['revenue'])
            movie.id = row['id']    
        self.close_cursor()
        self.db_disconnect
        return movie

    def find_by_id(self,id):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT * FROM movies where id = {} LIMIT 1".format(id))
        cursor.execute(query)
        results = cursor.fetchall()
        movie = None 
        if cursor.rowcount == 1:
            row = results[0]
            movie = Movie(row['title'], row['original_title'], row['synopsis'], row['duration'], row['production_budget'], row['release_date'], row['vote_average'], row['revenue'])
            movie.id = row['id']
        self.close_cursor()
        self.db_disconnect
        return movie
    
    def find_all(self):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT * FROM movies ")
        cursor.execute(query)
        results = cursor.fetchall()
        self.close_cursor()
        self.db_disconnect
        movies = []
        for result in results: 
            movie = Movie(result['title'], result['original_title'], result['synopsis'], result['duration'], result['production_budget'], result['release_date'], result['vote_average'], result['revenue'])
            movie.id = result['id']
            movies.append(movie)
        return movies








