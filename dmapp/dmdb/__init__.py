from pymongo import MongoClient

client = MongoClient()

db = client.deskmeter
switches = db.switch