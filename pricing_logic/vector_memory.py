import json
import chromadb
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("quotes")

model = SentenceTransformer("all-MiniLM-L6-v2")

def add_quote_to_memory(quote_id, transcript_text, quote_json):
    embedding = model.encode(transcript_text).tolist()
    
    # Only allowed: string, int, float, bool, None
    flat_metadata = {
        "quote_id": quote_id,
        "city": quote_json.get("city"),
        "zone": quote_json.get("zone"),
        "overall_total": quote_json.get("overall_total"),
        "confidence_score": quote_json.get("confidence_score"),
        "quote_json": json.dumps(quote_json)  # store as string
    }

    collection.add(
        ids=[quote_id],
        embeddings=[embedding],
        documents=[transcript_text],
        metadatas=[flat_metadata]
    )


def search_similar_quotes(transcript_text, top_k=3):
    embedding = model.encode(transcript_text).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results
