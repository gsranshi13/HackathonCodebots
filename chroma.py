import chromadb

client = chromadb.PersistentClient(path="testFolder/data")

client.heartbeat() # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
# client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.

collection = client.get_or_create_collection(name="test")





