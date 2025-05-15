# Filename: api/serve.py

import logging
from typing import List, Tuple

from fastapi import FastAPI
from pydantic import BaseModel, Field

from nlp.retrieve.retrieval_chain import create_retrieval_qa_chain

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


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


# Initialize the ConversationalRetrievalChain once
qa_chain = create_retrieval_qa_chain()


@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    logger.info("Received new chat request.")
    logger.debug(f"Request data: {request.dict()}")

    try:
        logger.info("Processing question through the QA chain.")

        # Pass user input into the chain
        response = qa_chain({"question": request.question})

        logger.info("QA chain processed the question.")
        logger.debug(f"Response from QA chain: {response}")
        logger.debug(f"Raw response keys: {list(response.keys())}")

        # Extract the correct fields
        result = response.get("answer", "No result found")
        updated_chat_history = qa_chain.memory.chat_memory.messages

        # Optional diagnostic: for future debugging
        logger.debug("Extracted answer: %s", result)
        logger.debug("Updated chat_history: %s", updated_chat_history)

        # Final response payload
        return {
            "answer": result,
            "chat_history": updated_chat_history,
            "memory_output": {"answer": result},
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
