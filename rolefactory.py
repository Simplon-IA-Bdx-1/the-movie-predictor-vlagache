import dbfactory

class RoleFactory(dbfactory.DbFactory):


    # pourrait retourner un objet role ? 
    def find_id(self,role):
        # cnx = self.db_connect()
        cursor = self.create_cursor()
        query = ("SELECT id FROM roles where name = '{}'".format(role))
        cursor.execute(query)
        results = cursor.fetchall()
        self.close_cursor()
        self.db_disconnect
        return results[0]['id'] # Retourne l'id lié à un role
