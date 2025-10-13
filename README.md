# Python Interview Repo

This project uses a virtual environment created with `uv` and installs Flask via `uv pip`.

## Features
- **Client Import Logic:**
   - The `import_client_handler` method in `helper.py` processes client imports, handling creation and updates based on integration data.
   - It supports matching clients by integration ID, email, or phone number, and updates client records if they already exist.

- **Unit Testing:**
   - The file `test_import_client_handler.py` contains unit tests for the import logic, verifying both client creation and update scenarios using an in-memory SQLite database.

## Quickstart
1. ** Install UV if you don't have it **
   ```zsh
    pip install uv
    ```
2. ** Create your virtualenv **
   ```zsh 
   uv venv ```
   ```
3. **Activate the virtual environment:**
    ```zsh
    source .venv/bin/activate
    ```
4. **Install Packages:**
    ```zsh
    uv pip install -r requirements.txt
    ```

## Requirements
- Python 3.12+
- uv (for venv and pip)
- Flask
- Flask-SQLAlchemy

## Files
- `app.py`: Main Flask application and models
- `helper.py`: Import logic and helper classes
- `test_import_client_handler.py`: Unit tests for client import logic
- `.venv/`: Virtual environment

---

For development, keep your virtual environment activated.
