import logging
from nlp.retrieve.retrieval_chain import create_retrieval_qa_chain
from config.defaults import CONFIG

# Set up basic logging to see what's going on
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Simulate a function to test each memory type
def test_memory(memory_type: str):
    CONFIG["MEMORY"]["type"] = memory_type
    qa_chain = create_retrieval_qa_chain()

    query_1 = "What is LangChain?"
    query_2 = "How does conversational memory work?"

    logger.info(f"Testing memory type: {memory_type}")

    response_1 = qa_chain.invoke({"question": query_1, "chat_history": []})
    logger.info(f"Response 1: {response_1['answer']}")

    response_2 = qa_chain.invoke({"question": query_2, "chat_history": response_1['chat_history']})
    logger.info(f"Response 2: {response_2['answer']}")

    memory_state = qa_chain.memory.chat_memory.messages
    logger.info(f"Memory state after second query: {memory_state}")

    if memory_type == "window":
        k = CONFIG["MEMORY"].get("window_size", 3)
        max_messages = k * 2
        assert len(memory_state) <= max_messages, (
            f"Expected memory window to store at most {max_messages} messages, "
            f"but got {len(memory_state)}"
        )
    elif memory_type == "summary_buffer":
        assert len(memory_state) > 0, "Expected some conversation summary in the memory"
    else:
        assert len(memory_state) > 0, "Expected chat history to be stored in memory"

    logger.info(f"Test for memory type '{memory_type}' completed.")


# Test all memory types
def run_tests():
    for memory_type in ["buffer", "window", "summary_buffer"]:
        test_memory(memory_type)

if __name__ == "__main__":
    run_tests()
