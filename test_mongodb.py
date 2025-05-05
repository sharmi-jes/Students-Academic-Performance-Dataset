
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://manikantaanyum966:admin123@cluster0.rvzge3r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# # This should now work
print("Databases:", client.list_database_names())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)