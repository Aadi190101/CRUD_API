import random, string
from .pymongo import id_collection


def generate_random_string(id_type, length=10):

    letters_and_digits = string.ascii_letters + string.digits

    id = "".join(random.choice(letters_and_digits) for i in range(length))
    while id_collection.find_one({"id": id, "id_type": id_type}):
        id = "".join(random.choice(letters_and_digits) for i in range(length))

    id_obj = {"id": id, "id_type": id_type}
    id_collection.insert_one(id_obj)

    return id
