#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import sys
import csv
import requests
import random
import os


from bs4 import BeautifulSoup
import time 
from movie import Movie
from person import Person
from tmdb import Tmdb
from dbmanager import DbManager
from moviefactory import MovieFactory
from peoplefactory import PeopleFactory
from rolefactory import RoleFactory
from moviepeoplerolefactory import MoviePeopleRoleFactory
from setparser import Parser

api_key = os.environ['TMDB_API_KEY']
tmdb = Tmdb(api_key)

moviefactory = MovieFactory()
peoplefactory = PeopleFactory()
rolefactory = RoleFactory()
moviepeoplerolefactory = MoviePeopleRoleFactory()

parser = Parser()
args = parser.set_parser()

    
def print_person(people):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def print_movie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))


if args.context == "people":
    if args.action == "list":
        people = peoplefactory.find_all()
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                print_person(person)
    if args.action == "find":
        peopleId = args.id
        person = peoplefactory.find_by_id(peopleId)
        if(person == None):
            print(f"Aucune personne avec l'id {peopleId} n'a été trouvé")
        else:
            print_person(person)
    if args.action == "insert":
        if args.firstname and args.lastname:
            person = Person(args.firstname, args.lastname)
            peoplefactory.insert(person)

if args.context == "movies":
    if args.action == "list":
        movies = moviefactory.find_all()  
        for movie in movies:
            print_movie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = moviefactory.find_by_id(movieId)
        if(movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé")
        else:
            print_movie(movie)
    if args.action == "insert":
        if args.title:
            movie = Movie(args.title, args.original_title, args.synopsis, args.duration, args.production_budget,  args.release_date, args.vote_average, args.revenue)
            moviefactory.insert(movie)
    if args.action == "import":
        if args.file:
            with open(args.file) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in reader:
                    movie = Movie(row['title'], row['original_title'], row['synopsis'], row['duration'], row['production_budget'], row['release_date'], row['vote_average'], row['revenue'])
                    moviefactory.insert(movie)
        if args.api == "themoviedb":
            print("... Recherche sur TMDB ...")
            if args.tmdbId:
                movie, people = tmdb.get_film(args.tmdbId) # renvoie movie et une liste d'acteur !!! peut renvoyer None
                if movie != None:
                    moviefactory.insert(movie)
                    print(f"Le film {movie.title} à bien été ajouté ! [ id : {movie.id}] ")
                    i = 0
                    for person in people:
                        if not peoplefactory.find_person_by_name(person): 
                            peoplefactory.insert(person)
                        role_id = rolefactory.find_id(person.role)
                        if person.id == None : 
                            person_sql = peoplefactory.find_person_by_name(person)
                            person.id = person_sql[0]['id']
                        moviepeoplerolefactory.insert(movie.id,person.id,role_id)
                        i += 1 
                    print(f"avec {i} personnes ( Casting / Equipe )")
                else:
                    print("Le film n'existe pas dans la DB de TMDB")
            if args.year:
                start = time.time()
                movies , people_list = tmdb.get_films_by_year(args.year) # Liste de films , et liste de liste de person
                print("Ajout a la base de données")
                already_db =  0
                i = 0
                film = 0
                cast = 0
                for movie in movies: # a chaque nouveau movie , people_list[i]
                    if moviefactory.find_by_tmdb_id(movie.tmdb_id):
                        already_db += 1 
                    else:
                        moviefactory.insert(movie)
                        film += 1
                        for person in people_list[i]: # Liste de person
                            if not peoplefactory.find_person_by_name(person): 
                                peoplefactory.insert(person)
                                cast += 1
                            role_id = rolefactory.find_id(person.role)
                            if person.id == None:
                                person_sql = peoplefactory.find_person_by_name(person)
                                person.id = person_sql[0]['id']
                            moviepeoplerolefactory.insert(movie.id,person.id,role_id)       
                        i += 1 
                print(f"Films ajoutés : {film}")
                print(f"Membres du casting ajoutés : {cast}")
                print(f"Films déja présents dans la DB : {already_db}")
                end = time.time()
                time_taken = (end - start)/60
                print(f"Durée de la requete {time_taken} minute(s)")

