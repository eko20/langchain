
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS


embeddings_model = OpenAIEmbeddings(api_key="")

#split log data by every newline
with open("formatted_logs.txt") as f:
    log = f.read()
    separators=[
        "\n"
    ],
    
    text_splitter = RecursiveCharacterTextSplitter(
    length_function=len,
    is_separator_regex=False,
    chunk_size=500,
)
    
texts = text_splitter.create_documents([log])

store = LocalFileStore("./cache/") #store

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    embeddings_model, store, namespace=embeddings_model.model
)

#test 
#print(list(store.yield_keys()))

db = FAISS.from_documents(texts, cached_embedder)

# Veritabanını kaydedin
db.save_local("faiss_index")


query = "404 error form apple computer"
docs = db.similarity_search(query)
print(docs[0].page_content)
print(docs[1].page_content)
print(docs[2].page_content)