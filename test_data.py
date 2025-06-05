
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://raghavbankar2023:7kyxzAWAb6hREOHT@mystore.qlh0vm2.mongodb.net/?retryWrites=true&w=majority&appName=MyStore"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)