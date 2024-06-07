import mysql.connector
from random import randint
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
random_query = "SELECT * FROM projects WHERE status IS NULL ORDER BY RAND(%s) LIMIT %s OFFSET %s"
add_query = "INSERT INTO projects (title, description) VALUES (%s, %s)"

def get(num=1, seed=None, page=0):
    if seed is None:
        seed = randint(0, 100000)
    cursor.execute(random_query, (seed,num,page*num))
    return cursor.fetchall()

def print_project(project):
    print(f"Title: {project[1]}")
    print(f"Description: {project[2]}")
    print()

def random(num=1):
    list = get(num) 
    for project in list:
        print_project(project) 

def queue(num):
    # Want to replace with better algorithm than completely random
    list = get(num, randint(0, 100000), 0)
    for i, project in enumerate(list):
        print(f"Project {i+1} of {num}")
        print(f"Title: {project[1]}")
        print(f"Description: {project[2]}")
        print("-----------------------------------------")
        print("Commands: [S]ave, [D]elete, [Next], [Quit]")
        opt = input("Enter an option: ")
        # TODO add functionality to save delete and quit

def add():
    name = input("Project name: ")
    desc = input("Project description: ")
    cursor.execute(add_query, (name, desc))
    connector.commit()

def help():
    print("Options:")
    print("[A]dd a new project")
    print("[R]andomly select a project")
    print("[S]earch for a project")
    print("[Q]uit")
    print()

def input_loop(leaving=False):
    try:
        args = str(input("Choose an option (? for help): ")).lower().split(' ')
        if args[0][0] == '?':
            help()
        elif args[0][0] == 'a':
            add()
        elif args[0][0] == 'r':
            if len(args) > 1: 
                random(int(args[1]))
            else:
                random()
        input_loop()
    except KeyboardInterrupt:
        if leaving:
            # Closing logic here
            connector.close()
            print("\nClosing...")
            exit(0)
        print("\n^C again to close")
        input_loop(True)
     
input_loop()
