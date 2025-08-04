from pymongo import AsyncMongoClient

from config import MONGO_APP, MONGO_DB, MONGO_PASS, MONGO_URI, MONGO_USER

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_URI}/?retryWrites=true&w=majority&appName={MONGO_APP}"
# Create a new client and connect to the server
client = AsyncMongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client[MONGO_DB]
