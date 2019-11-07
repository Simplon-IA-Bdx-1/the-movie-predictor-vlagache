import requests
import json 
from pprint import pprint
from movie import Movie
from person import Person
from random import randint 


with open('tmdbapikey.txt', 'r') as file:
    api_key = file.read()


url = 'https://api.themoviedb.org/3/'

# C'est l'heure pour une nouvelle astuce @here :)
# Pour faciliter la gestion des SELECT, INSERT ou UPDATE de vos entité, une bonne pratique est de créer une classe genre "MovieFactory" dont le rôle est de récupérer, ajouter ou mettre à jour vos entités dans votre base. Cela donnerai :

# movie = MovieFactory.findOneByImdbId(imdb_id)
# movie.synopsis = "blabla mis à jour"
# MovieFactory.update(movie)

# ou

# movie = Movie(title, original_title, ...)
# MovieFactory.insert(movie)


class Tmdb:
    
    # def __init__(self, url):
    #     self.url = url
  
    def get_film(self,id):
        page = requests.get(f"{url}movie/{id}?api_key={api_key}&append_to_response=credits")
        content = page.json()
        
        if 'status_code' not in content : 

            #### Infos générale sur le film 
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

            #### Casting #### 
            people = []
            print( "Casting : " + content['title'])
            casting = content['credits']['cast']
            for actor in casting:
                for i in range(0, 11):
                    if actor['order'] == i:
                        str_name = actor['name']
                        str_name_split = str_name.split()
                        firstname = str_name_split[0]
                        lastname = str_name_split[1]
                        person = Person(firstname, lastname)
                        people.append(person)
            return movie, people
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

    def get_casting(self,id):
        page = requests.get(f"{url}movie/{id}?api_key={api_key}&append_to_response=credits")
        content = page.json()
        people = []
        print( "Casting : " + content['title'])
        casting = content['credits']['cast']
        for actor in casting:
            for i in range(0, 11):
                if actor['order'] == i:
                    str_name = actor['name']
                    str_name_split = str_name.split()
                    firstname = str_name_split[0]
                    lastname = str_name_split[1]
                    person = Person(firstname, lastname)
                    people.append(person)
        return people