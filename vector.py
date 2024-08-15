from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from openai import OpenAI



# OpenAI Embeddings modelini oluşturun
api_key = ""

embeddings_model = OpenAIEmbeddings(api_key=api_key)


# FAISS veritabanını yükleyin
db = FAISS.load_local("faiss_index", embeddings=embeddings_model, allow_dangerous_deserialization=True)

# Retriever'ı oluşturun
retriever = db.as_retriever(search_kwargs={"k": 5})


client = OpenAI(api_key=api_key)

def generate_augmented_response(query):
    docs = retriever.invoke(query)
    print("GPT'ye gönderilen loglar:")
    
    
    search_results = "\n\n".join([doc.page_content for doc in docs])
    print(search_results)
    print("\n")
    
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant to control logs, before every answer there will be logs you will answer the question based on provided logs"},
            {"role": "user", "content": search_results},
            {"role": "user", "content": query}
        ]
    )
    
    return completion.choices[0].message.content

# Terminal tabanlı sürekli sorgulama döngüsü
while True:
    query = input("Question (type 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    
    print("\n")
    
    response = generate_augmented_response(query)
    print(f"Cevap: {response}")



