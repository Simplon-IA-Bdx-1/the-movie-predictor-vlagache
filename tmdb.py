import requests
import json
import os
from pprint import pprint
from movie import Movie
from person import Person
from random import randint 


url = 'https://api.themoviedb.org/3'


class Tmdb:
    
    def __init__(self, api_key):
        self.api_key = api_key

    def get_film(self,id):
        

        content = self.content_movie_by_id(id) # Json de toutes les infos d'un film par ID 
        movie = self.get_infos(content) # movie = obj movie Or None 
        people = self.get_casting(content) # people = list obj person or None 

        return movie, people

    def content_movie_by_id(self,id):
        
        page = requests.get(f"{url}/movie/{id}?api_key={self.api_key}&append_to_response=credits")
        content = page.json()
        return content 

    def content_movies_by_year(self,year):

        page = requests.get(f"{url}/discover/movie?api_key={self.api_key}&primary_release_year={year}&vote_count.gte=1000")
        content = page.json()
        return content

    def content_movies_by_release(self,date,now):
        page = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&language=en-US&primary_release_date.gte={date}&primary_release_date.lte={now}&with_runtime.gte=60")
        content = page.json()
        return content

    def get_infos(self,content):

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
            return movie
        return None 
    
    def get_casting(self,content): 

        ####### Casting      
        people = []
        if 'status_code' not in content : 
            casting = content['credits']['cast']
            for actor in casting:
                for i in range(0, 11):
                    if actor['order'] == i:
                        str_name = actor['name']
                        person = self.str_to_person(str_name)
                        person.role = 'actor'
                        people.append(person)

            ###### Crew 
            crew = content['credits']['crew']
            for person in crew:
                if person['job'] == 'Director':
                        str_name = person['name']
                        person = self.str_to_person(str_name)
                        person.role = 'director'
                        people.append(person)
                elif person['department'] == 'Sound' and person['job'] == 'Original Music Composer':
                        str_name = person['name']
                        person = self.str_to_person(str_name)
                        person.role = 'composer'
                        people.append(person)
            return people
        return None

    def str_to_person(self,str):
        str_split = str.split()
        firstname = str_split[0].replace("'", "")
        if len(str_split) == 1: # Pour remedier au probleme des acteurs sans nom de famille 
            lastname = "Doe"
        elif len(str_split) == 3: # 2 Noms de famille ,  Helena Bonham Carter
             lastname = str_split[1].replace("'", "") + " " + str_split[2].replace("'", "")
        else:
            lastname = str_split[1].replace("'", "")
        person = Person(firstname,lastname)
        return person

    def get_films_by_year(self,year):

        # On cherche des films de l'année year avec + de 4000 votes
        # On recupere le nombre total de pages 
        nb_page = 1
        i = 0
        content = self.content_movies_by_year(year)
        total_pages = content['total_pages']
        movies_id = []
        movies = []
        people_list = []

        # Boucle sur toutes les pages pour récuperer les id de tout les films correspondant à la recherche 
        # Id dans la liste movies_id 
        while nb_page <= total_pages:
            url_req = f"{url}/discover/movie?api_key={self.api_key}&primary_release_year={year}&vote_count.gte=1000&page={nb_page}"
            page = requests.get(url_req)
            content = page.json()
            results = content['results']
            for movie in results:
                movies_id.append(movie['id'])
                i += 1
            nb_page += 1

        # On va chercher les infos pour chaque id de film 
        for id in movies_id:
            movie, people = self.get_film(id)
            movies.append(movie)
            people_list.append(people)
         
        return movies,people_list # Liste de films , Liste de liste de person

    def get_films_by_release(self,date,now):
        
        # On cherche des films de l'année year avec + de 4000 votes
        # On recupere le nombre total de pages 
        nb_page = 1
        i = 0
        content = self.content_movies_by_release(date,now)
        total_pages = content['total_pages']
        movies_id = []
        movies = []
        people_list = []

        # Boucle sur toutes les pages pour récuperer les id de tout les films correspondant à la recherche 
        # Id dans la liste movies_id 
        while nb_page <= total_pages:
            url_req = f"https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&language=en-US&primary_release_date.gte={date}&primary_release_date.lte={now}&with_runtime.gte=60&page={nb_page}"
            page = requests.get(url_req)
            content = page.json()
            results = content['results']
            for movie in results:
                movies_id.append(movie['id'])
                i += 1
            nb_page += 1

        # On va chercher les infos pour chaque id de film 
        for id in movies_id:
            movie, people = self.get_film(id)
            movies.append(movie)
            people_list.append(people)
         
        return movies,people_list # Liste de films , Liste de liste de person

