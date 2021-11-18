from data.db_conn import db_auth
from services.models import User, Pet

graph = db_auth()

def find_user(email):
    user = User.match(graph, f"{email}")
    return user

#Create a new user account in the database and return the user object. First validate if the user already exists.
def create_user(first_name, last_name, email, password):
    
    if find_user(email):
        return None
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = password
    graph.create(user)
    return user

def create_pet(name, species, owner):
    pet = Pet()
    pet.name = name
    pet.species = species
    pet.owner = owner
    graph.create(pet)
    return pet


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


def get_profile(user_id):
    # user = User.match(graph, f"{usr}").first()
    user_profile = graph.run(f"MATCH (x:User) WHERE x.email='{user_id}' RETURN x.first_name as name, x.email as email").data()
    return user_profile