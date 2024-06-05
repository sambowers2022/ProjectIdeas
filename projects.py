import mysql.connector
import os
from dotenv import load_dotenv 

load_dotenv()
connector = mysql.connector.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PWD"),
    host='localhost',
    database='projects'
)
cursor = connector.cursor()
random_query = "SELECT * FROM projects WHERE status IS NULL ORDER BY RAND() LIMIT 1"
add_query = "INSERT INTO projects (title, description) VALUES (%s, %s)"

def random():
    cursor.execute(random_query)
    print(cursor.fetchone())

def add():
    name = input("Project name: ")
    desc = input("Project description: ")
    cursor.execute(add_query, (name, desc))

def input_loop():
    opt = None
    try:
        opt = str(input("Choose an option (? for help): ")).lower()[0]
    except IndexError:
        input_loop() 
    except KeyboardInterrupt:
        print("\nClosing...")
        exit(0)
    if opt == '?':
        print("Options:")
        print("[A]dd a new project")
        print("[R]andomly select a project")
        print("[S]earch for a project")
        print("[Q]uit")
        print()
    elif opt == 'a':
        add()
    elif opt == 'r':
        random()
    input_loop()
     
input_loop()
