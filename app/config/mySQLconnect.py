import pymysql, pymysql.cursors # a cursor is the object we use to interact with the database

# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root', 
            password = 'root',#YOUR PASSWORD HERE INSTEAD OF 'root'
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor, # specifices the format to return our data to be in the form of dictionaries
            autocommit = True
        )
    def run_query(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data) # combine data and with our query 
                print("Running Query:", query) # print out the query, to ensure it looks the way we expect it to
                cursor.execute(query) # make sure data isn't being passed in!
                if query.strip().lower().startswith("insert"): # trim removes extra whitespace at the beginning and end of our queries, and lower turns everything lowercase
                    return cursor.lastrowid # return the id of the row we just inserted
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall() # return all matching rows as a list of dictionaries 
            except Exception as e:
                print("MySQL query has failed:", e) # if our query fails, we should see this in our terminal!
                return False # return False if our query fails
            finally:
                self.connection.close()

def connect(db):
    return MySQLConnection(db)