# Filename: api/server.py

import logging
from typing import List, Tuple

from fastapi import FastAPI
from pydantic import BaseModel, Field

from nlp.retrieve.retrieval_chain import create_retrieval_qa_chain

# Set up logging
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


# Initialize QA chain at startup
qa_chain = create_retrieval_qa_chain()


@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    # Log incoming request data
    logger.info("Received new chat request.")
    logger.debug(f"Request data: {request.dict()}")

    try:
        # Log before calling the qa_chain
        logger.info("Processing question through the QA chain.")
        response = qa_chain(
            {"question": request.question, "chat_history": request.chat_history}
        )

        # Log the response from qa_chain
        logger.info("QA chain processed the question.")
        logger.debug(f"Response from QA chain: {response}")

        # Extract result (answer) and updated chat history
        result = response.get("answer", "No result found")
        updated_chat_history = response.get("chat_history", [])

        # Log extracted details
        logger.debug(f"Extracted answer: {result}")
        logger.debug(f"Updated chat_history: {updated_chat_history}")

        # Create memory output with only the answer (no source_documents)
        memory_output = {
            "answer": result,
        }

        # Return the response with only the necessary information
        return {
            "answer": result,  # Return the answer directly
            "chat_history": updated_chat_history,  # Updated chat history for the session
            "memory_output": memory_output,  # Internal memory tracking output with just the answer
        }

    except Exception as e:
        # Log the exception if anything goes wrong
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return {"error": "An error occurred while processing your request."}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
