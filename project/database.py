from psycopg2 import pool 
import constants as c 

class Database:
    __connection_pool = None #belongs to the class itself, NOT one of the objects
    
    @staticmethod
    def initialize(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(
                                            1, 
                                            10,
                                            **kwargs)   

    @classmethod
    def get_connection(cls):
        if cls.__connection_pool == None:
            Database.initialize(database=c.DATABASE_NAME, host=c.DATABASE_HOST, user=c.DATABASE_USER, password=c.DATABASE_PASSWORD)
        return cls.__connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, ext_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)
        