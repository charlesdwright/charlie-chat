### To-Do: Add Title Metadata to Document Chunks

- **Goal**: Modify the chunking process to include the document title (e.g., as the filename) in the metadata for each chunk.

- **Impact**:
  1. **Metadata in Vector Store**: Each chunk will contain document title metadata, improving traceability.
  2. **Query Output**: Titles will be available in search results to provide context on where each chunk came from.
  3. **Contextual Relevance**: Titles can help with ranking and filtering search results based on the document.
  4. **Performance**: Slight increase in storage size and minimal impact on query speed.
  5. **Consistency**: Ensure filenames are sanitized for consistency and avoid conflicts.
  6. **Ingestion Complexity**: Slight increase in ingestion time but minimal for small to medium datasets.

- **Action**: Update `chunker.py` to add title metadata to each chunk when processing documents.


## **Project To-Do List**

### **1. Setup Conda for Environment Isolation and Dependency Management**

-   **Install Conda**  (Miniconda or Anaconda).

-   **Create a clean environment**  for both the frontend (Streamlit) and backend (FastAPI) to avoid dependency conflicts:

    -   Frontend Environment:  `streamlit-ui`

    -   Backend Environment:  `backend-env`

-   **Install dependencies**  for both frontend and backend:

    -   For  **Frontend**  (`streamlit`  and any UI-related packages).

    -   For  **Backend**  (`fastapi`,  `torch`,  `chromadb`,  `requests`,  `pydantic`,  `langchain`, etc.).

-   **Export environments**  to ensure reproducibility:

    -   Frontend:  `conda env export > frontend-environment.yml`

    -   Backend:  `conda env export > backend-environment.yml`

-   **Share environments**  via  `environment.yml`  for easy installation on other machines.


### **2. Backend (FastAPI + LangChain)**

-   Ensure backend is properly set up with FastAPI for handling requests to the LangChain-powered backend.

-   Verify correct implementation of the  **ConversationalRetrievalChain**  and integrate logging and diagnostics for backend requests.


### **3. Streamlit Frontend Setup**

-   Set up the  **Streamlit**  frontend with chat functionality.

-   Connect the frontend to the FastAPI backend to process user messages via API requests.

-   Implement  **session memory**  and  **message history**  to persist chat.
