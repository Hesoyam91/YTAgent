from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DeterministicFakeEmbedding

def get_song_context(query, db_path="./chroma_db"):
    # Cargamos la base de datos persistente
    vector_db = Chroma(
        persist_directory=db_path, 
        embedding_function=DeterministicFakeEmbedding(size=1536)
    )
    results = vector_db.similarity_search(query, k=3)
    return " / ".join([doc.page_content for doc in results])