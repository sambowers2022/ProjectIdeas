import mysql.connector
import os
from dotenv import load_dotenv 
from random import randint
import datetime 

# Query templates
random_query = "SELECT * FROM projects WHERE status IS NULL ORDER BY RAND(%s) LIMIT %s OFFSET %s"
add_query = "INSERT INTO projects (title) VALUES (%s)"
list_query = "select title, avg(rating) as avg,count(*) as num from ratings join projects on project_id=projects.id group by projects.id order by avg desc, num desc LIMIT %s OFFSET %s"
rate_query = "INSERT INTO ratings (project_id, rating) VALUES (%s, %s)"
delete_query = ""

class DataBase:
    connector = None
    cursor = None
    def __init__(self):
        load_dotenv()
        DataBase.connector = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PWD"),
            host='localhost',
            database='projects'
        )
        DataBase.cursor = self.connector.cursor(dictionary=True)

    def get_list(self, num=10, page=0):
        self.cursor.execute(list_query, (num, page*num))
        return self.cursor.fetchall()

    def rate(self, id, rating):
        self.cursor.execute(rate_query, (id, rating))
        self.connector.commit()

    def get_random(self, num=1, seed=None, page=0):
        if seed is None:
            seed = randint(0, 100000)
        self.cursor.execute(random_query, (seed,num,page*num))
        return self.cursor.fetchall()

    def delete(self, id):
        pass

    def close(self):
        self.cursor.close()
        self.connector.close()
