import chromadb
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"guru-benchmark-4cfaf5e8357e.json"

client = chromadb.PersistentClient(path="/tmp/data")

client.heartbeat() # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
# client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.

collection = client.get_or_create_collection(name="test")





