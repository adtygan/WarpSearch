# https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from subprocess import check_output
import argparse

os.environ['CURL_CA_BUNDLE'] = ''

class VectorStore:
    _client = None  # Class-level attribute to hold the persistent client
    _db_path = 'db/'
    _collection = None # Class-level attribute to hold the collection
    _cln_name = 'library'

    _sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

    @classmethod
    def get_collection(cls):
        """
        Get the collection from ChromaDB. If the client 
        or collection does not exist, initialize them.
        :return: The ChromaDB collection.
        """
        if cls._client is None:
            cls._client = chromadb.PersistentClient(path=cls._db_path)  # Initialize the client if it doesn't exist
        if cls._collection is None:
            cls._collection = cls._client.get_or_create_collection(
                name=cls._cln_name,
                embedding_function=cls._sentence_transformer_ef,
                metadata={"hnsw:space": "cosine"}
            )
        return cls._collection
    
    def add(self, image_path):
        """
        Add a new image to the ChromaDB collection.
        :param image_path: The path to the image file.
        :param description: The description of the image.
        """
        collection = self.get_collection()  # Ensure the client is initialized
        description = check_output(f'blip-caption "{image_path}"', shell=True).decode('utf-8').strip().split('\n')
        # description is a list
        log_file_path = './fswatch.log'
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"[File Added] {image_path}\n   └── [Caption] {description[0]}\n")
        desc_embedding = self._sentence_transformer_ef(description)
        collection.add(
            embeddings=desc_embedding,
            documents=[description],
            metadatas=[{"filename": image_path}],
            ids = [str(collection.count() + 1)]
        )       

    def query(self, query_text):
        """
        Query the ChromaDB collection with the given query text.        
        :param query_text: The text to query the collection with.
        :return: List of results matching the query.
        """
        collection = self.get_collection()
        results = collection.query(
            query_texts=[query_text],
            n_results=2
        )
        return results
    
    def purge(self):
        """
        Wipe out all entries in the vector store by deleting the collection
        """
        try:
            (self._client).delete_collection(self._cln_name)  # Clear all entries in the collection
        except:
            pass
        with open('./fswatch.log', 'a') as log_file:
            log_file.write("\n\n\n------------------\n[All entries purged]\n------------------\n\n\n")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add an image to the ChromaDB collection.')
    parser.add_argument('image_path', type=str, help='The path to the image file.')
    args = parser.parse_args()

    vector_store = VectorStore()
    vector_store.add(args.image_path)
