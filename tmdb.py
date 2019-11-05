import requests
import json 
from pprint import pprint
from movie import Movie
from random import randint 


with open('tmdbapikey.txt', 'r') as file:
    api_key = file.read()


url = 'https://api.themoviedb.org/3/'


class Tmdb:
    
    # def __init__(self, url):
    #     self.url = url
  
    def get_film(self,id):
        page = requests.get(f"{url}movie/{id}?api_key={api_key}")
        content = page.json()

        # si il y'a status_code dans le .json le film n'est pas trouvé sinon on crée un film 
        
        if 'status_code' not in content : 
            title = content['title'].replace("'", " ")

            if 'original_title' in content:
                original_title = content['original_title'].replace("'", " ")
            else:
                original_title = title
            
            synopsis = content['overview'].replace("'", " ")
            production_budget = content['budget']
            tmdb_id = content['id']
            vote_average = content['vote_average']
            revenue = content['revenue']

            if content['runtime'] == None:
                duration = 0
            else:
                duration = content['runtime']

            if content['release_date'] == '':
                release_date = None
            else:
                release_date = content['release_date']


            movie = Movie(title, original_title, synopsis, duration, production_budget, release_date, vote_average, revenue)
            movie.tmdb_id = tmdb_id
            return movie
        return None 


    def get_random_films(self,n): # n films randoms
        movies = []
        i = 1
        while i <= int(n):
            index = randint(1,30000)
            if self.get_film(index) != None:
                movie = self.get_film(index)
                movies.append(movie)
            else:
                i -= 1
            i += 1
        return movies


    def get_rating(self, id):
        page = requests.get(f"{url}movie/{id}/release_dates?api_key={api_key}")
        content = page.json()  
        for x in content['results'] :
            if x['iso_3166_1'] == 'FR':
                rating = x['release_dates'][0]['certification']
                print(rating)
