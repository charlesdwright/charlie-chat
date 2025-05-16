import logging
from typing import List, Tuple

from fastapi import FastAPI
from pydantic import BaseModel, Field

from config.defaults import CONFIG  # Assuming your config is here
from nlp.retrieve.retrieval_chain import create_retrieval_qa_chain

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Read return_source_documents flag from configuration
return_source_documents = CONFIG["CHAIN"].get("return_source_documents", False)
logger.debug(f"return_source_documents value from config: {return_source_documents}")


# ----- Added chat_id to request model -----
class QueryRequest(BaseModel):
    question: str = Field(..., example="What is this project about?")
    chat_history: List[Tuple[str, str]] = Field(
        default=[],
        example=[
            ["Hi", "Hello! How can I help you?"],
            [
                "What is this project?",
                "It's a chatbot using LangChain and Cloudflare's LLM.",
            ],
        ],
    )
    chat_id: str = Field(..., example="abc-123-session-id")


# ----- End of change -----


# ----- Initialize QA chain map (per chat_id memory) -----
qa_chain_map = {}  # Stores qa_chain instances per chat_id
# ----- End of change -----


@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    logger.info("Received new chat request.")
    logger.debug(f"Request data: {request.dict()}")

    try:
        query = request.question
        chat_history = request.chat_history
        chat_id = request.chat_id

        logger.info(f"Processing question for chat_id: {chat_id}")

        # ----- Create/reuse QA chain with memory per chat_id -----
        if chat_id not in qa_chain_map:
            logger.debug(f"No chain found for chat_id={chat_id}, creating new one.")
            qa_chain_map[chat_id] = create_retrieval_qa_chain()
        qa_chain = qa_chain_map[chat_id]
        # ----- End of change -----

        # Step 1: Retrieve the relevant documents based on the query
        retrieved_docs = qa_chain.retriever.get_relevant_documents(query)
        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query}")

        # Step 2: Combine the question and retrieved documents into a single input string
        input_data = (
            query + "\n\n" + "\n".join([doc.page_content for doc in retrieved_docs])
        )
        logger.debug(
            f"Input data being passed to QA chain: {input_data[:500]}..."
        )  # Preview first 500 chars

        # Step 3: Prepare the input payload with the correct format
        input_payload = {
            "question": input_data,
            "chat_history": chat_history,
        }
        logger.debug(f"Input payload to qa_chain.invoke: {input_payload}")

        # Step 4: Invoke the chain and get the raw response
        raw_response = qa_chain.invoke(input_payload)

        logger.info("QA chain processed the question.")
        logger.debug(f"Raw response from QA chain: {raw_response}")
        logger.debug(f"Raw response keys: {list(raw_response.keys())}")

        # Step 5: Save only the 'answer' in memory
        answer = raw_response.get("answer", "No answer found")
        qa_chain.memory.save_context({"question": query}, {"answer": answer})

        # Step 6: Log source documents if configured
        if return_source_documents and "source_documents" in raw_response:
            logger.info("Source documents used:")
            for i, doc in enumerate(raw_response["source_documents"], 1):
                metadata = doc.metadata
                content = doc.page_content
                logger.info(f"[{i}] Metadata: {metadata}")
                logger.info(f"[{i}] Content Preview: {content[:200]}...")

        # Step 7: Return response
        updated_chat_history = qa_chain.memory.chat_memory.messages
        return {
            "answer": answer,
            "chat_history": updated_chat_history,
            "memory_output": {"answer": answer},
            "source_documents": raw_response.get("source_documents", []),
        }

    except Exception as e:
        logger.error(
            f"Error occurred while processing the request:\n{e}", exc_info=True
        )
        return {"error": "An error occurred while processing your request."}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
