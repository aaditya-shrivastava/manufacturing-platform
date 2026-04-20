import chromadb
from openai import OpenAI
from datetime import datetime
import config

client    = OpenAI(api_key=config.OPENAI_API_KEY)
chroma    = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = chroma.get_or_create_collection(name="manufacturing_concepts")


def get_embedding(text: str) -> list[float]:
    """Convert text to a vector embedding using OpenAI."""
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def store_concept(user_prompt: str, narrative: str, image_path: str = None) -> str:
    """
    Store a manufacturing concept + its narrative in ChromaDB.

    Args:
        user_prompt:  Original user input
        narrative:    Generated text description
        image_path:   Local path to saved image (optional)

    Returns:
        The unique ID of the stored concept
    """
    concept_id = f"concept_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    embedding  = get_embedding(user_prompt + " " + narrative)

    collection.add(
        ids        =[concept_id],
        embeddings =[embedding],
        documents  =[narrative],
        metadatas  =[{
            "user_prompt": user_prompt,
            "image_path":  image_path or "",
            "created_at":  datetime.now().isoformat()
        }]
    )
    return concept_id


def search_similar(query: str, n_results: int = 3) -> list[dict]:
    """
    Find the most similar past concepts to a given query.

    Args:
        query:     Search text
        n_results: How many similar results to return

    Returns:
        List of dicts with keys: id, narrative, metadata, distance
    """
    total = collection.count()
    if total == 0:
        return []

    n_results = min(n_results, total)
    embedding  = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "id":        results["ids"][0][i],
            "narrative": results["documents"][0][i],
            "metadata":  results["metadatas"][0][i],
            "distance":  results["distances"][0][i]
        })
    return output


def get_all_concepts() -> list[dict]:
    """Return all stored concepts from the DB."""
    total = collection.count()
    if total == 0:
        return []

    results = collection.get(include=["documents", "metadatas"])
    output  = []
    for i in range(len(results["ids"])):
        output.append({
            "id":        results["ids"][i],
            "narrative": results["documents"][i],
            "metadata":  results["metadatas"][i]
        })
    return output
