from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import json
import os

class CodeExampleRetriever:
    def __init__(self, persist_dir: str = './chroma_db', collection_name: str = 'etl_examples'):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=persist_dir))
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)
    
    def add_examples(self, examples: List[Dict[str, str]]):
        docs = [f"{ex['instruction']} {ex.get('input', '')}" for ex in examples]
        metas = [{'code': ex['output'], 'instruction': ex['instruction']} for ex in examples]
        ids = [f'ex_{i}' for i in range(len(examples))]
        self.collection.add(documents=docs, metadatas=metas, ids=ids)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.collection.count() == 0:
            return []
        results = self.collection.query(query_texts=[query], n_results=min(top_k, self.collection.count()))
        return [{'instruction': results['metadatas'][0][i]['instruction'], 'code': results['metadatas'][0][i]['code'], 'relevance': 1.0} 
                for i in range(len(results['ids'][0]))] if results['ids'][0] else []
    
    def load_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.add_examples(json.load(f))
