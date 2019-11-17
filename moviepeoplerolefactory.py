import dbfactory

class MoviePeopleRoleFactory(dbfactory.DbFactory):


    def insert(self,movie_id,person_id,role_id):
        cursor = self.create_cursor()
        add_moviepeoplerole = ("INSERT INTO movies_people_roles "
                    "(movies_id, people_id, role_id)"
                     "VALUES (%s, %s, %s)")
        data_moviepeoplerole =  (movie_id , person_id , role_id)
        cursor.execute(add_moviepeoplerole, data_moviepeoplerole)
        self.commit()
        self.close_cursor()
        self.db_disconnect


