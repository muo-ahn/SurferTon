1. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the application

Start the FastAPI server using Uvicorn:
```sh
cd server_side
uvicorn app.main:app --reload
