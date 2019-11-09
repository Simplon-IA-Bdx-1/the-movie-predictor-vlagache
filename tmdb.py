import requests
import json
import os
from pprint import pprint
from movie import Movie
from person import Person
from random import randint 


url = 'https://api.themoviedb.org/3/'


class Tmdb:
    
    def __init__(self, api_key):
        self.api_key = api_key

    def get_film(self,id):

        content = self.connect_tmdb_by_id(id) # Json de toutes les infos d'un film par ID 
        movie = self.get_infos(content) # movie = obj movie Or None 
        people = self.get_casting(content) # people = list obj person or None 

        return movie,people

    def connect_tmdb_by_id(self,id):
        
        page = requests.get(f"{url}movie/{id}?api_key={self.api_key}&append_to_response=credits")
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
                        str_name_split = str_name.split()
                        firstname = str_name_split[0]
                        lastname = str_name_split[1]
                        person = Person(firstname, lastname)
                        person.role = 'acteur'
                        people.append(person)

            ###### Crew 
            crew = content['credits']['crew']
            for person in crew:
                if person['job'] == 'Director':
                        str_name = person['name']
                        person = self.str_to_person(str_name)
                        person.role = 'realisateur'
                        people.append(person)
                elif person['department'] == 'Sound' and person['job'] == 'Original Music Composer':
                        str_name = person['name']
                        person = self.str_to_person(str_name)
                        person.role = 'compositeur'
                        people.append(person)
            return people
        return None

    def str_to_person(self,str):
        str_split = str.split()
        firstname = str_split[0]
        lastname = str_split[1]
        person = Person(firstname,lastname)
        return person

    

    # def get_random_films(self,n): # n films randoms

        
    #     # movies = []
    #     # people = []
    #     # i = 1 

    #     # while i <= int(n):
    #     #     index = randint(1,30000)
    #     #     movie, people = self.get_film(index)
    #     #     if movie != None:
    #     #         movie = self


    #     movies = []
    #     peoples = []
    #     i = 1
    #     while i <= int(n):
    #         index = randint(1,30000)
    #         if self.get_film(index) != None:
    #             movie = self.get_film(index)
    #             movies.append(movie)
    #         else:
    #             i -= 1
    #         i += 1
    #     return movies


    # def get_rating(self, id):
    #     page = requests.get(f"{url}movie/{id}/release_dates?api_key={api_key}")
    #     content = page.json()  
    #     for x in content['results'] :
    #         if x['iso_3166_1'] == 'FR':
    #             rating = x['release_dates'][0]['certification']
    #             print(rating)

