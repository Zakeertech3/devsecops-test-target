import os
from pathlib import Path
from typing import Any, Dict, Iterator

import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

def get_elasticsearch_client() -> Elasticsearch:
    return Elasticsearch(
        os.environ["ELASTIC_ENDPOINT"],
        api_key=os.environ["ELASTIC_API_KEY"],
        request_timeout=120,
        max_retries=3,
        retry_on_timeout=True
    )

def configure_index(es_client: Elasticsearch, index_name: str, dimensions: int) -> None:
    index_mapping = {
        "mappings": {
            "properties": {
                "pr_number": {"type": "keyword"},
                "title": {"type": "text"},
                "body": {"type": "text"},
                "title_vector": {
                    "type": "dense_vector",
                    "dims": dimensions,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
        
    es_client.indices.create(index=index_name, body=index_mapping)

def document_generator(
    dataframe: pd.DataFrame, 
    embedding_model: SentenceTransformer, 
    target_index: str
) -> Iterator[Dict[str, Any]]:
    for _, row in dataframe.iterrows():
        pr_title = str(row.get("title", ""))
        pr_body = str(row.get("body", ""))
        
        vector_embedding = embedding_model.encode(pr_title).tolist()
        
        yield {
            "_index": target_index,
            "_source": {
                "pr_number": str(row.get("id", "")),
                "title": pr_title,
                "body": pr_body,
                "title_vector": vector_embedding
            }
        }

def main() -> None:
    load_dotenv()
    
    data_filepath = Path("./data/all_pull_request.parquet")
    target_index = "pr-code-reviews"
    vector_dimensions = 384
    
    es_client = get_elasticsearch_client()
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    configure_index(es_client, target_index, vector_dimensions)
    
    dataframe = pd.read_parquet(data_filepath)
    
    success_count, failed_count = helpers.bulk(
        es_client, 
        document_generator(dataframe, embedding_model, target_index),
        chunk_size=100,
        request_timeout=120,
        stats_only=True
    )
    
    print(f"Documents indexed: {success_count}")
    if failed_count:
        print(f"Failed to index: {failed_count}")

if __name__ == "__main__":
    main()