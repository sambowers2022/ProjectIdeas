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
random_query = "SELECT * FROM projects WHERE status IS NULL ORDER BY RAND() LIMIT %s"
add_query = "INSERT INTO projects (title, description) VALUES (%s, %s)"

def random(num=1):
    cursor.execute(random_query, (num,))
    for project in cursor.fetchall():
        print(f"Title: {project[1]}")
        print(f"Description: {project[2]}")
        print()

def add():
    name = input("Project name: ")
    desc = input("Project description: ")
    cursor.execute(add_query, (name, desc))
    connector.commit()

def input_loop(leaving=False):
    try:
        args = str(input("Choose an option (? for help): ")).lower().split(' ')
    except KeyboardInterrupt:
        if leaving:
            # Closing logic here
            connector.close()
            print("\nClosing...")
            exit(0)
        print("\n^C again to close")
        input_loop(True)
    if args[0][0] == '?':
        print("Options:")
        print("[A]dd a new project")
        print("[R]andomly select a project")
        print("[S]earch for a project")
        print("[Q]uit")
        print()
    elif args[0][0] == 'a':
        add()
    elif args[0][0] == 'r':
        if len(args) > 1: 
            random(int(args[1]))
        else:
            random()
    input_loop()
     
input_loop()
