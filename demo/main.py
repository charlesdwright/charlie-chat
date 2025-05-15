# main.py

from fastapi import FastAPI
from langserve import add_routes
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from nlp.llms.cloudflare import CloudflareLLM, CloudflareEmbeddings
from langchain.vectorstores import Chroma

# ---- Set up retriever ----
embedding_model = CloudflareEmbeddings()
vectordb = Chroma(
    persist_directory="nlp/persist/db/chroma",
    collection_name="document_collection",
    embedding_function=embedding_model
)
retriever = vectordb.as_retriever()

# ---- Set up memory ----
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ---- Set up chain ----
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=CloudflareLLM(),
    retriever=retriever,
    memory=memory,
    return_source_documents=False,
)

# ---- FastAPI + LangServe ----
app = FastAPI()
add_routes(app, qa_chain, path="/chat")

# ---- To run: uvicorn main:app --reload ----
