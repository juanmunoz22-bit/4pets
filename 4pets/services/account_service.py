from data.db_conn import db_auth
from services.models import User

graph = db_auth()

def find_user(email):
    user = User.match(graph, f"{email}").first()
    return user

#Create a new user account in the database and return the user object. First validate if the user already exists.
def create_user(email, password, first_name, last_name):
    if find_user(email):
        return None
    user = User()
    user.email = email
    user.password = password
    user.first_name = first_name
    user.last_name = last_name
    graph.create(user)
    return user

#Create a function for user login.
def login_user(email, password):
    user = User.match(graph, f"{email}").first()
    if not user:
        print("User not found")
        return None
    if user.password == password:
        return user
    else:
        print("Password is incorrect")
        return None
