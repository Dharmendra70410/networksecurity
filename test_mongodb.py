
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://guptadharmendra182003_db_user:Boss%40123@cluster0.tbxjnhp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)