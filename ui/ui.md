
### ✅  **Cheat-Sheet: Making the Backend URL Configurable**

Here’s how to do it cleanly in your Streamlit  `streamlit_app.py`:

#### 1. Add a  `config.toml`  file

Create:  `~/.streamlit/config.toml`  or  `ui/config.toml`

    toml
    # ui/config.toml  [backend]  url = "http://localhost:8000/chat"

#### 2. Read it using Python

    python
    import toml import os # Default fallback DEFAULT_BACKEND_URL = "http://localhost:8000/chat"
    # Try to load from config
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        config = toml.load(config_path)
        BACKEND_URL = config.get("backend", {}).get("url", DEFAULT_BACKEND_URL) except Exception:
        BACKEND_URL = DEFAULT_BACKEND_URL`

✅ You can now change the URL  **without touching the code**.


Yes, the  **UI**  and  **backend**  can be deployed on the  **same server**. In this setup:

-   **Backend**  runs on one port (e.g.,  `5000`).

-   **UI**  (e.g.,  **Streamlit**) runs on another port (e.g.,  `8501`).


The UI communicates with the backend using  **local URLs**  like:

- `http://localhost:5000`

Each service should have  **separate configuration files**:

-   `ui/config.py`  for  **UI settings**.

-   `backend/config.py`  for  **backend settings**.


You can also have shared configurations (e.g., API URLs) in a  **common directory**.

For  **production**:

-   Use a  **reverse proxy**  (e.g.,  **Nginx**  or  **Apache**) to route traffic to the appropriate service.


This setup simplifies  **deployment and management**  by keeping both services on the same machine with minimal networking complexity.

**Sensitive data**  and  **environment-specific configurations**  can be managed using  **environment variables**  or a  `.env`  file.
