"""
rag_pipeline.py
End-to-end RAG for folder-based documents with improved chunking.
Requires: transformers, sentence-transformers, faiss-cpu, langchain, torch
"""

import os
import glob
from typing import List

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.text_splitter import RecursiveCharacterTextSplitter


class RAGPipeline:
    def __init__(
        self,
        data_dir: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_name: str = "google/flan-t5-base",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.data_dir = data_dir
        self.embedding_model = SentenceTransformer(embedding_model)
        self.llm_tokenizer = AutoTokenizer.from_pretrained(llm_name)
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(llm_name)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "?", "!"]
        )

        self.index = None
        self.id_to_text = {}

    def load_documents(self) -> List[str]:
        files = glob.glob(os.path.join(self.data_dir, "**"), recursive=True)
        docs = []
        for f in files:
            if os.path.isfile(f):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        docs.append(fp.read())
                except Exception:
                    pass
        return docs

    def build_index(self):
        docs = self.load_documents()
        chunks = []
        for doc in docs:
            chunks.extend(self.text_splitter.split_text(doc))

        embeddings = self.embedding_model.encode(chunks, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.id_to_text = {i: chunk for i, chunk in enumerate(chunks)}

    def retrieve(self, query: str, k: int = 4) -> List[str]:
        query_emb = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_emb, k)
        return [self.id_to_text[i] for i in indices[0]]

    def generate_answer(self, query: str, retrieved_chunks: List[str]) -> str:
        context = "\n".join(retrieved_chunks)
        prompt = (
            "Answer the question based only on the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\nAnswer:"
        )
        inputs = self.llm_tokenizer(prompt, return_tensors="pt")
        outputs = self.llm.generate(**inputs, max_new_tokens=256, do_sample=False)
        return self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)

    def ask(self, query: str, k: int = 4) -> str:
        retrieved = self.retrieve(query, k)
        return self.generate_answer(query, retrieved)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run RAG on local folder")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to folder with documents")
    parser.add_argument("--query", type=str, required=True, help="Your question")
    args = parser.parse_args()

    rag = RAGPipeline(data_dir=args.data_dir)
    rag.build_index()

    answer = rag.ask(args.query)
    print("\nAnswer:\n", answer)
