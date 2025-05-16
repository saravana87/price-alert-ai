import pandas as pd
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, Document
import os
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def load_query_engine():
    import pandas as pd
    df = pd.read_csv("products.csv")

    documents = []
    for _, row in df.iterrows():
        text = "\n".join(f"{col}: {row[col]}" for col in df.columns)
        documents.append(Document(text=text))

    embed_model = OpenAIEmbedding()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    return index.as_query_engine()
