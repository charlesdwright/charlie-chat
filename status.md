### **Milestone 1**

### ✅ Current Task Status (Updated)

-   **Step 1: Environment setup and API keys**  – ✅ Done

-   **Step 2: Embedding object and Chroma vector store**  – ✅ Done

-   **Step 3: LangChain setup and conversational retrieval chain**  – ✅ Complete

-   **Step 4: FastAPI server setup**  – ⚙️ Functional; endpoints working

-   **Step 5: Deployment with Uvicorn**  – ✅ Verified via local test (`localhost:8000/docs`)


----------

### ✅ Immediate Next Steps (Updated)

#### Step 3: Finalizing LangChain Conversational Chain –  **✅ Done**

-   **Accomplishments**:

    -   Refactored  `retrieval_chain.py`  to use a config-driven  `diagnostic_mode`  that toggles  `return_source_documents`.

    -   Memory handled via  `ConversationBufferMemory`, integrated and working.

    -   Confirmed chat history persists and updates correctly via  `qa_chain.memory.chat_memory.messages`.

-   **Testing**:

    -   Successfully ran  `tests/test_chain.py`  with realistic input (e.g., "What is this project about?").

    -   Fixed hallucination-related bugs by ensuring correct parsing of LLM responses.


#### Step 4: FastAPI Server Setup –  **✅ Base Implementation Done**

-   **Accomplishments**:

    -   Fully implemented  `/chat`  route in  `api/serve.py`.

    -   Logs include QA chain response, chat history, and diagnostics (if enabled).

    -   Ready for optional  `/history`  endpoint and further features (e.g., clear session, diagnostics toggle).


#### Step 5: Deployment with Uvicorn –  **✅ Verified Locally**

-   **Accomplishments**:

    -   `api/serve.py`  includes  `uvicorn.run(...)`  block.

    -   Confirmed server launch and  `/docs`  UI accessibility.

    -   Endpoint tested via browser, ready for  `curl`  or Postman usage.


----------

### 🚧 Additional Enhancements (Planned)

1.  **Add  `diagnostic_mode`**: ✅ Now config-driven in  `defaults.py`.

2.  **Chat history persistence**: 💡 Consider writing to disk/session store for long-term sessions.

3.  **Log sanitization**: 🚨 Current logs include full user/LLM content — needs redaction for production use.

4.  **/history endpoint**: 💬 Optional for exposing chat memory (future task).


### **Milestone 2**

1.  **Setup**:

    -   Import necessary modules (`streamlit`  and  `requests`).

    -   Configure the Streamlit app properties.

2.  **Preparing the Chat Infrastructure**:

    -   Initialize a session state variable to store chat messages.

    -   Set up the display mechanism for chat messages using Streamlit’s  `st.chat_message`  component.

3.  **Generate Response**:

    -   Define the  `generate_response`  function to handle HTTP requests to the backend, send the user message, and get a response from the LLM.

    -   Capture user input and append it to the message history in session state.

4.  **Check Message Roles**:

    -   Check the role of the last message in the history.

    -   If the message is not from the assistant, call  `generate_response`  to process and get the assistant's response.

5.  **Real-Time Chat**:

    -   Continuously listen for user input and update the chat interface with responses to simulate an interactive chat experience.
