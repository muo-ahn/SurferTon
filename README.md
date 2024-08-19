# My FastAPI Project

This is a simple FastAPI project setup.

## Installation

1. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the application

Start the FastAPI server using Uvicorn:
```sh
uvicorn app.main:app --reload
```