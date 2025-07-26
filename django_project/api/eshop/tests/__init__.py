import os
from pathlib import Path
from dotenv import load_dotenv  # You might need to pip install python-dotenv

# Find the path to your .env file relative to the tests directory
# Assuming .env is in django_project/
env_path = Path(__file__).resolve().parent.parent.parent / '.env'  # Path from eshop/tests/__init__.py up to django_project/.env

if env_path.exists():
    load_dotenv(str(env_path))  # Load the environment variables from .env
    print(f"DEBUG: Loaded .env file from {env_path}")  # For debugging purposes

# Now, try importing the plugin as before
pytest_plugins = ['pytest_django']
