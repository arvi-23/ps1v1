from pymongo import MongoClient
conn_string=f"mongodb+srv://ard23:8$AI13vanaja@cluster0.ldcwmsp.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(conn_string)
dbb=client.ard3
collection=dbb.login_v1
