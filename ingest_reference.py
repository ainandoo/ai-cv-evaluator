"""
Stub script to ingest reference documents (Job Description, Case Study Brief, Scoring Rubric)
into ChromaDB. Will chunk PDFs, embed, and persist to DB.
"""
import os
import chromadb


def ingest_reference_docs():
  client = chromadb.PersistentClient(path="vector_store")
  collection = client.get_or_create_collection("reference_docs")


# TODO: parse PDFs from ./data/reference/
docs = [
{"id": "doc1", "text": "Sample job description content..."},
{"id": "doc2", "text": "Sample case study brief..."}
]


for doc in docs:
  collection.add(documents=[doc["text"]], ids=[doc["id"]])


if __name__ == "__main__":
  ingest_reference_docs()