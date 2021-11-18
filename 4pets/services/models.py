from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

#Create a User class that inherits from GraphObject with the label "user" and the properties "username" and "password" and "email" and pets relationship that is related to the user.
class User(GraphObject):
    __primarylabel__ = "User"
    __primarykey__ = "email"
    first_name = Property()
    last_name = Property()
    email = Property()
    password = Property()
    pets = RelatedTo("Pet", "HAS_PET")

#Pet class has the label "pet" and the properties "name" and "species" and "owner" relationship that is related to the user.
class Pet(GraphObject):
    __primarykey__ = "name"
    name = Property()
    species = Property()
    owner = RelatedFrom("User", "HAS_PET")