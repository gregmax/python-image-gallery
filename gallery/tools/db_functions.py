import psycopg2
import json
import boto3, botocore
from gallery.tools.secrets import get_secret_image_gallery
from gallery.tools.config import S3_BUCKET, S3_LOCATION

db_name = "image_gallery"

connection = None
S3 = None

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

def s3_connect():
    global S3
    S3 = boto3.client("s3")

# Change password to get_password function later
def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    connection.set_session(autocommit=True)


# Retrieve one user
def list_user(user):
    global connection
    cur = connection.cursor()
    data = (user,)

    # Grab single user from DB
    cur.execute("SELECT username, password, full_name FROM users WHERE username=%s", data)
    
    # Set data to results
    results = cur.fetchone()
    # Close cursor and return to menu
    #connection.close()
    return results

# Retrieve list of users
def list_users():
    global connection
    cur = connection.cursor()

    # Grab all users for DB and store in results
    cur.execute("SELECT username, full_name FROM users")
    results = cur.fetchall()
    
    # Close connection and return results
    #connection.close()
    return results

# Retrieve user info for login
def login(user, password):
    global connection
    cur = connection.cursor()
    data = (user, password)

    sql_statement = "SELECT username, password FROM users WHERE username=%s AND password=%s;"

    # Grab single user from DB
    cur.execute(sql_statement, data)
    
    # Set data to results
    results = cur.fetchone()
    #connection.close()

    if results is None:
        return None
    else:
        return results


# Create new user
def add_user(user, password, fullname):
    global connection
    cur = connection.cursor()

    # Store input in tuple
    data = (user, password, fullname)

    # SQL statements
    sql_statement1 = "INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s);"

    # Check to see if username already exists in DB
    cur.execute(select_all_users)
    results = cur.fetchall()

    for record in results:
        if user == record[0]:
            print("Error: user with username " + user + " already exists")
            # Close connection and return
            #connection.close()
            return
    else:
        cur.execute(sql_statement1, data)
        # Save new user record to DB
        connection.commit()
        # Close connection and return
        #connection.close()
        return


# Update user
def edit_user(username, password, fname):
    global connection
    cur = connection.cursor()
    
    # SQL statements
    sql_statement1 = "UPDATE users SET password=%s, full_name=%s WHERE username=%s;"
    sql_statement2 = "UPDATE users SET full_name=%s WHERE username=%s;"
    sql_statement3 = "UPDATE users SET password=%s WHERE username=%s;"

    cur.execute(select_all_users)
    # Check to see if username already exists in DB
    results = cur.fetchall()

    for record in results:
        if username == record[0]:
            if len(password) == 0 and len(fname) > 0:
                cur.execute(sql_statement2, (fname, username))
                connection.commit()
                #connection.close()
                return
            elif len(password) > 0 and len(fname) == 0:
                cur.execute(sql_statement3, (password, username))
                connection.commit()
                #connection.close()
                return
            elif len(password) == 0 and len(fname) == 0:
                print("No changes will be made to user " + user);
                #connection.close()
                return
            elif len(password) > 0 and len(fname) > 0:
                cur.execute(sql_statement1, (password, fname, username))
                connection.commit()
                #connection.close()
                return
    else:
        print("No such user.")
        #connection.close()
        return


# Delete user
def delete_user(username):
    global connection
    cur = connection.cursor()
    data = (username,)

    # SQL statements
    sql_statement1 = "DELETE FROM users WHERE username=%s;"

    # cur.execute(sql_statement2)
    # for record in cur:
    # if user != record[0]:
    # print(user + " not found.")
    # 
    # connection.close()

    # Delete the user
    cur.execute(sql_statement1, data)
    connection.commit()
    #connection.close()
    return

# Upload user file to S3
def upload_file_to_s3(file, bucket, username):
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, bucket, str(username) + '/{}'.format(file.filename))
    return

# Retrieve image URLs from S3
def get_files_from_s3(bucket, username):
    s3_client = boto3.resource('s3')
    contents = []
    bucket = s3_client.Bucket(bucket)
    objects = bucket.objects.filter(Prefix= str(username) + '/')
    for obj in objects:
        key = obj.key
        url = 'https://s3.amazonaws.com/'+ str(bucket) + '/' + str(key)
        contents.append(url)
    return contents
    
