#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import mysql.connector
import sys
import argparse
import csv
import requests
import random
import os


from bs4 import BeautifulSoup
import time 
from movie import Movie
from person import Person
from tmdb import Tmdb


def connectToDatabase():
    password = os.environ['MYSQL_PASSWORD']
    return mysql.connector.connect(user='predictor', password=password,
                              host='database', #127.0.0.1
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findFilmByTmdbIdQuery(tmbdId):
    return("SELECT * FROM movies where tmdb_id = {}".format(tmbdId))

def findPeopleByFirstnameQuery(firstname,lastname):
    return("SELECT * FROM people where firstname = '{}' and lastname = '{}'".format(firstname,lastname))

def findIdByRoleQuery(role):
    # print("SELECT id FROM roles where role = {}".format(role))
    return("SELECT id FROM roles where name = '{}'".format(role))
    
def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {} LIMIT 1 ".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def insertPeopleQuery(person):
    add_person = ("INSERT INTO people"
               "(firstname, lastname) "
               "VALUES (%s , %s)")

    data_person = (person.firstname , person.lastname)
    return add_person , data_person

def insertMovieQuery(movie):
    add_movie = ("INSERT INTO movies "
               "(title, original_title, synopsis, duration, production_budget, release_date, vote_average, revenue, tmdb_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data_movie = (movie.title, movie.original_title, movie.synopsis, movie.duration, movie.production_budget, movie.release_date, movie.vote_average, movie.revenue, movie.tmdb_id)

    return add_movie , data_movie

def insertMoviePeopleRoleQuery(movie_id,person_id,role_id):
    add_moviepeoplerole = ("INSERT INTO movies_people_roles "
                    "(movies_id, people_id, role_id)"
                     "VALUES (%s, %s, %s)")
    data_moviepeoplerole =  (movie_id , person_id , role_id)

    return add_moviepeoplerole, data_moviepeoplerole


 
def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    entity = None 
    if(table == "movies"):
        if(cursor.rowcount == 1):
            row = results[0]
            entity = Movie(row['title'], row['original_title'] , row['synopsis'], row['duration'], row['production_budget'], row['release_date'])
            entity.id = row['id']
    if(table == "people"):
        if(cursor.rowcount == 1):
            row = results[0]
            entity = Person(row['firstname'], row['lastname'])
            entity.id = row['id']
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return entity 

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    if(table == "movies"):
        movies = []
        for result in results:
            movie = Movie(result['title'], result['original_title'], result['synopsis'], result['duration'],
            result['production_budget'], result['release_date'])
            movie.id = result['id']
            movies.append(movie)
        return movies
    elif (table =="people"):
        people = []
        for result in results:
            person = Person(result['firstname'], result['lastname'])
            person.id = result['id']
            people.append(person)
        return people
    

def find_film_by_imdb_id(id_tmdb):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findFilmByTmdbIdQuery(id_tmdb))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def find_people_by_firstname(firstname,lastname):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findPeopleByFirstnameQuery(firstname,lastname))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def find_id_by_role(role):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findIdByRoleQuery(role))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results[0]['id'] # Retourne l'id lié à un role

def insertPeople(person):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    add_person , data_person = insertPeopleQuery(person)
    cursor.execute(add_person, data_person)
    person.id = cursor.lastrowid
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def insertMovie(movie):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    add_movie , data_movie = insertMovieQuery(movie)
    cursor.execute(add_movie, data_movie)
    movie.id = cursor.lastrowid
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def insertMoviePeopleRole(id_movie,id_person,id_role):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    add_moviepeoplerole , data_moviepeoplerole = insertMoviePeopleRoleQuery(id_movie,id_person,id_role)
    cursor.execute(add_moviepeoplerole, data_moviepeoplerole)
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)


def printPerson(people):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))

# Parser 

parser = argparse.ArgumentParser(description='Process MoviePredictor data')
parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')
action_subparser = parser.add_subparsers(title='action', dest='action')


# [movies,people] list 
list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

# [movies,people] find id 
find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un parametre')
find_parser.add_argument('id' , help='Identifant Ã  rechercher')

#  movies import --file newfile.csv
import_parser = action_subparser.add_parser('import', help='importer un fichier csv dans la DB')
import_parser.add_argument('--file' , help='file.csv')
import_parser.add_argument('--api' , help='Api utilisé pour importer des films')

# --api themoviedb --imdbId ID 
know_args = parser.parse_known_args()[0]
if know_args.api == "themoviedb" : 
    import_parser.add_argument('--random' , help='n films random')
    import_parser.add_argument('--tmdbId' , help='Id du film tmdb')

insert_parser = action_subparser.add_parser('insert', help='Insere une entité dans la database')
scrap_parser = action_subparser.add_parser('scrap', help='scrap les infos d\'un film sur Wikipedia')


if know_args.context == "people":
    # [movies,people] insert [title,duration,orginal-title,rating,release-date,synopsis,production-budget, marketing-budget|firstname,lastname]
    insert_parser.add_argument('--firstname', help='Prénom', required=True)
    insert_parser.add_argument('--lastname', help='Nom de famille', required=True)

if know_args.context == "movies":
    insert_parser.add_argument('--title', help='Titre', required=True)
    insert_parser.add_argument('--duration', help='Durée du film', required=True)
    insert_parser.add_argument('--original-title', help='Titre original', required=True)
    insert_parser.add_argument('--rating', help='Classement du film', required=True)
    insert_parser.add_argument('--release-date', help='Date de sortie', required=True)
    insert_parser.add_argument('--synopsis', help='Synopsis', required=True)
    insert_parser.add_argument('--production-budget', help='Budget production', required=True)
    insert_parser.add_argument('--marketing-budget', help='Budget Marketing', required=True)

    # movies scrap URL fiche film Wiki

    scrap_parser.add_argument('url', help='url de la page wiki à scraper')

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        person = find("people", peopleId)
        if(person == None):
            print(f"Aucune personne avec l'id {peopleId} n'a été trouvé")
        else:
            printPerson(person)
    if args.action == "insert":
        if args.firstname and args.lastname:
            person = Person(args.firstname, args.lastname)
            insertPeople(person)

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = find("movies", movieId)
        if(movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé")
        else:
            printMovie(movie)
    if args.action == "insert":
        if args.title:
            # --marketing-budget NULL ne fonctionne pas => Incorrect integer value: '' for column 'marketing_budget' at row 1
            movie = Movie(args.title, args.original_title, args.synopsis, args.duration, args.production_budget,  args.release_date)
            insertMovie(movie)
    if args.action == "import":
        if args.file:
            with open(args.file) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in reader:
                   insertMovie(row['title'], row['original_title'], row['duration'], row['rating'], row['release_date']) # Le fichier csv n'a pas de synopsis etc..
        if args.api == "themoviedb":
            print("... Recherche sur TMDB ...")
            if args.tmdbId:
                tmdb = Tmdb()
                movie, people = tmdb.get_film(args.tmdbId) # renvoie movie et une liste d'acteur !!! peut renvoyer None
                if movie != None:
                    insertMovie(movie)
                    print(f"Le film {movie.title} à bien été ajouté ! ")
                    i = 0
                    for person in people:
                        if not find_people_by_firstname(person.firstname,person.lastname):
                            insertPeople(person)
                        role_id = find_id_by_role(person.role)
                        if person.id == None : 
                            person_sql = find_people_by_firstname(person.firstname, person.lastname)
                            person.id = person_sql[0]['id']
                        insertMoviePeopleRole(movie.id,person.id,role_id)
                        i += 1 
                    print(f"avec {i} acteurs")
                else:
                    print("Le film n'existe pas dans la DB de TMDB")
            if args.random:
                tmdb = Tmdb()
                movies = tmdb.get_random_films(args.random)
                print("Ajout a la bse de données")
                i = 0
                already_db =  0
                for movie in movies:
                    if find_film_by_imdb_id(movie.tmdb_id):
                        already_db += 1 
                    else :
                        insertMovie(movie)
                        print(f"{i} - {movie.title}")
                        i += 1 
                print(f"ajout films dans la db : {i}")
                print(f"films deja présent dans la db : {already_db}")



      
