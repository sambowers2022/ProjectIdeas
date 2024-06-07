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

def confirm(action):
    try:
        if input(f"\nAre you sure you want to {action}? [Y]es or ^C to confirm: ").lower()[0] == 'y':
            return True
    except KeyboardInterrupt:
        print()
        return True
    except IndexError:
        pass
    return False

def print_project(project):
    print(f"Title: {project[1]}")
    print(f"Description: {project[2]}")
    print()

def random(num=1):
    list = get(num) 
    for project in list:
        print_project(project) 

def rate(id, rating):
    cursor.execute("INSERT INTO ratings (project_id, rating) VALUES (%s, %s)", (id, rating))
    connector.commit()

def queue(num=10):
    # Want to replace with better algorithm than completely random
    list = get(num, randint(0, 100000), 0)
    for i, project in enumerate(list):
        print("---------------------------------------------------")
        print(f"Project {i+1} of {num}")
        print("---------------------------------------------------")
        print(f"Title: {project[1]}")
        print(f"Description: {project[2]}")
        print("---------------------------------------------------")
        print("Enter a rating (1-9) or [S]kip, [D]elete, [Q]uit")
        print("---------------------------------------------------")
        while True:
            try:
                opt = input("Enter an option: ").lower()[0]
                if opt == 's':
                    break
                elif opt == 'd':
                    if confirm(f"delete {project[1]}"):
                        delete(project[0])
                        break
                elif opt == 'q':
                    raise KeyboardInterrupt
                elif opt.isdigit() and int(opt) > 0:
                    rate(project[0], opt)
                    break
                else:
                    print("Invalid input")
            except KeyboardInterrupt:
                if confirm("leave queue"):
                    return
                continue
def add():
    try:
        name = input("Project name: ")
        desc = input("Project description: ")
        cursor.execute(add_query, (name, desc))
        connector.commit()
    except KeyboardInterrupt:
        print()
        return

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
        elif args[0][0] == 'q':
            queue()
        elif args[0][0] == 'r':
            if len(args) > 1: 
                random(int(args[1]))
            else:
                random()
        input_loop()
    except KeyboardInterrupt:
        if confirm("exit") is True:
            connector.close()
            print("Closing...")
            exit(0)
        input_loop()
     
input_loop()
