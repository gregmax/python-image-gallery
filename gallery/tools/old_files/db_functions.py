import psycopg2
import json
from secrets import get_secret_image_gallery

db_name = "image_gallery"

connection = None

select_all_users = "SELECT * FROM users"

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']

# Change password to get_password function later
def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    connection.set_session(autocommit=True)


# Read list of users
def list_users():
    global connection
    cur = connection.cursor()

    # Grab all users for DB and print results
    cur.execute(select_all_users)

    print('username\tpassword\tfull name')

    print('-----------------------------------------')

    results = cur.fetchall()
    for row in results:
        print("{: <15} {: <15} {: <15}".format(*row))
    # Close cursor and return to menu
    
    connection.close()
    return


# Create new user
def add_user():
    global connection
    cur = connection.cursor()

    # Ask user for input and store input
    user = str(input("Username> "))
    password = str(input("Password> "))
    fullname = str(input("Full Name> "))
    data = (user, password, fullname)

    # SQL statements
    sql_statement1 = "INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s);"

    # Check to see if username already exists in DB
    cur.execute(select_all_users)
    results = cur.fetchall()

    for record in results:
        if user == record[0]:
            print("Error: user with username " + user + " already exists")
            # Close cursor and return to menu
            
            connection.close()
            return
    else:
        cur.execute(sql_statement1, data)
        # Save new user record to DB
        connection.commit()
        # Close cursor and return to menu
        
        connection.close()
        return


# Update user
def edit_user():
    global connection
    cur = connection.cursor()

    # Ask user for input
    user = str(input("Username> "))
    
    # SQL statements
    sql_statement1 = "UPDATE users SET password=%s, full_name=%s WHERE username=%s;"
    sql_statement2 = "UPDATE users SET full_name=%s WHERE username=%s;"
    sql_statement3 = "UPDATE users SET password=%s WHERE username=%s;"

    cur.execute(select_all_users)
    # Check to see if username already exists in DB
    results = cur.fetchall()

    for record in results:
        if user == record[0]:
            password = str(input("New password (press enter to keep current)> "))
            fullname = str(input("New full name (press enter to keep current)> "))
            if len(password) == 0 and len(fullname) > 0:
                cur.execute(sql_statement2, (fullname, user))
                connection.commit()
                connection.close()
                return
            elif len(password) > 0 and len(fullname) == 0:
                cur.execute(sql_statement3, (password, user))
                connection.commit()
                connection.close()
                return
            elif len(password) == 0 and len(fullname) == 0:
                print("No changes will be made to user " + user);
                connection.close()
                return
            elif len(password) > 0 and len(fullname) > 0:
                cur.execute(sql_statement1, (password, fullname, user))
                connection.commit()
                connection.close()
                return
    else:
        print("No such user.")
        connection.close()
        return


# Delete user
def delete_user():
    global connection
    cur = connection.cursor()
    user = str(input("Enter username to delete> "))
    confirm = str(input("Are you sure that you want to delete " + user + "? "))
    data = (user,)

    # SQL statements
    sql_statement1 = "DELETE FROM users WHERE username=%s;"

    # cur.execute(sql_statement2)
    # for record in cur:
    # if user != record[0]:
    # print(user + " not found.")
    # 
    # connection.close()

    # Delete the user upon confirmation
    if confirm.lower() in ['yes', 'y']:
        cur.execute(sql_statement1, data)
        connection.commit()
        print('Deleted.')
        connection.close()
        return
    else:
        # Delete the user upon confirmation
        print(user + " will not be deleted")
        
        connection.close()
        return
