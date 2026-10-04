import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_PROJECTS_ENDPOINT")
AGENT_NAME = os.getenv( "AGENT_NAME","research-agent")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

if not PROJECT_ENDPOINT:
    raise ValueError("PROJECT_ENDPOINT is missing from .env")

if not VECTOR_STORE_ID:
    raise ValueError("Vector_store_id is missing from .env")