from modules.database.database import all_collections
from modules.database.validation import validate_database

def flush_all_collections():
    """Flush all collections by deleting all documents in each collection."""
    for collection in all_collections:
        collection.delete_many({})
        print(f"Flushed collection: {collection.name}")
    validate_database()

if __name__ == "__main__":
    flush_all_collections()
