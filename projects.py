from random import randint
import database 

db = database.DataBase()

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

def print_list(list, fields=None):
    if fields is None:
        fields = list[0].keys()
    for item in list:
        for field in fields:
            print(f"{field}: " + str(item[field]))


def random(num=1):
    list = db.get_random(num) 
    print_list(list, ["title"])


def queue(num=10):
    # Want to replace with better algorithm than completely random
    list = db.get_random(num, randint(0, 100000), 0)
    for i, project in enumerate(list):
        print("---------------------------------------------------")
        print(f"Project {i+1} of {num}")
        print()
        print(project)
        print()
        print("---------------------------------------------------")
        print("Enter a rating (1-9) or [S]kip, [D]elete, [Q]uit")
        while True:
            try:
                opt = input("Enter an option: ").lower()[0]
                if opt == 's':
                    break
                elif opt == 'd':
                    if confirm(f"delete {project['title']}"):
                        db.delete(project['title'])
                        break
                elif opt == 'q':
                    raise KeyboardInterrupt
                elif opt == 'l':
                    print()
                elif opt.isdigit() and int(opt) > 0:
                    db.rate(project['id'], opt)
                    break
                else:
                    print("Invalid input")
            except KeyboardInterrupt:
                if confirm("leave queue"):
                    return
                continue
            except:
                print("Invalid input")
        print("\n")

def add():
    try:
        name = input("Project name: ")
        cursor.execute(add_query, (name,))
        connector.commit()
    except KeyboardInterrupt:
        print()
        return

def help():
    print("Options:")
    print("[A]dd a new project")
    print("[R]andomly select a project")
    print("[Q]ueue")
    print()

def input_loop(leaving=False):
    try:
        args = str(input("Choose an option (? for help): ")).lower().split(' ')
        opt = args[0][0]
        if opt == '?':
            help()
        elif opt == 'a':
            add()
        elif opt == 'q':
            queue()
        elif opt == 'r':
            if len(args) > 1: 
                random(int(args[1]))
            else:
                random()
        else:
            raise Exception
    except KeyboardInterrupt:
        if confirm("exit") is True:
            print("Closing...")
            db.close()
            print("Closed")
            exit(0)
    except Exception as e:
        print(e)
        print("Invalid input")
    input_loop()
     
input_loop()
