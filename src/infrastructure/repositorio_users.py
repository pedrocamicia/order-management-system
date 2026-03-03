from psycopg2.extensions import connection
from src.domain.user import User

class RepositorioUser:
    def __init__(self, conn : connection):
        self.conn = conn
    
    def map_user(self, row):
        
        return User(
            id=row[0],
            email=row[1],
            hashed_password=row[2],
            role=row[3]
        )
    
    #####################################################
    
    def create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    hashed_password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'customer'
                );
            """)
            self.conn.commit()
            
    #########################################################            
            
    def guardar_user(self, user : User):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id, role
                """, (user.email, user.hashed_password))
            
            row = cursor.fetchone()
            
            user.id = row[0]
            user.role = row[1]
            
            self.conn.commit()
            
            return user
            
    ##############################################################       
            
    def get_user_by_mail(self, mail : str):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users WHERE email = (%s)
                """, (mail,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            user = self.map_user(row)
            
            self.conn.commit()
            
            return user
        
    ##############################################################       
            
    def get_user_by_id(self, id : int):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users WHERE id = (%s)
                """, (id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            user = self.map_user(row)
            
            self.conn.commit()
            
            return user