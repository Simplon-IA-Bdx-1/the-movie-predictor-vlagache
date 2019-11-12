import dbfactory
from person import Person

class PeopleFactory(dbfactory.DbFactory):


    def insert(self,person):
        cnx = self.db_connect()
        cursor = self.create_cursor()
        add_person = ("INSERT INTO people"
               "(firstname, lastname) "
               "VALUES (%s , %s)")

        data_person = (person.firstname , person.lastname)
        cursor.execute(add_person, data_person)
        person.id = cursor.lastrowid
        # self.commit()
        cnx.commit()
        self.close_cursor()
        self.db_disconnect

    # Pourrait retourner un objet person
    def find_person_by_name(self,person):
        cursor = self.create_cursor()
        query = ("SELECT * FROM people where firstname = '{}' and lastname = '{}'".format(person.firstname,person.lastname))
        cursor.execute(query)
        results = cursor.fetchall()
        person = None
        if cursor.rowcount == 1:
            row = results[0]
            person = Person(row['firstname'], row['lastname'])
            person.id = row['id']
        self.close_cursor()
        self.db_disconnect
        return person
    
    def find_by_id(self,id):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT * FROM people where id = {} LIMIT 1".format(id))
        cursor.execute(query)
        results = cursor.fetchall()
        person = None 
        if cursor.rowcount == 1:
            row = results[0]
            person = Person(row['firstname'], row['lastname'])
            person.id = row['id']
        self.close_cursor()
        self.db_disconnect
        return person
    
    def find_all(self):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT * FROM people ")
        cursor.execute(query)
        results = cursor.fetchall()
        self.close_cursor()
        self.db_disconnect
        people = []
        for result in results: 
            person = Person(result['firstname'], result['lastname'])
            person.id = result['id']
            people.append(person)
        return people

    
    