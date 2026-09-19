## ALL SETTINGS IN ONE PLACE


import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_env(key: str, default=None):
    """Read a config value from Streamlit secrets (cloud) or .env (local)."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


## ENV VAR / SECRET

GROQ_API_KEY = get_env("GROQ_API_KEY")
JINA_API_KEY = get_env("JINA_API_KEY")

# GATEWAY API
PORTKEY_API_KEY = get_env("PORTKEY_KEY_API")

## GUARDRAILS LAYER

GUARD_MODEL_NAME = "openai/gpt-oss-safeguard-20b"

# tracing
LANGSMITH_TRACING = get_env("LANGSMITH_TRACING", "false")
LANGSMITH_ENDPOINT = get_env("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = get_env("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = get_env("LANGSMITH_PROJECT")


## DEFINE PATH - DATA / VECTOR STORE

DATA_FILE_PATH = os.path.join("data", "hr_policy.txt")

# migrating to cloud vector store, QDRANT

QDRANT_API_KEY = get_env("QDRANT_API_KEY")
QDRANT_URL = get_env("QDRANT_URL")
QDRANT_COLLECTION_NAME = get_env("QDRANT_COLLECTION_NAME", "hr_policy")  # this creates the cluster in the Qdrant website


## models
## LLM AND EMBEDDING MODEL

LLM_MODEL_NAME = "openai/gpt-oss-120b"

embeddings_model = "jina-embeddings-v2-base-en"

## CHUNK / TEXT SPLITTERS CONFIG

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

## RETRIEVAL RESULTS

TOP_K_RESULTS = 3

## SYSTEM INSTRUCTIONS

SYSTEM_PROMPT = (
    "You are a friendly HR assistant."
    "Always use the search_hr_policy tool to look up"
    "facts before answering"
    "If the answer isn't in the search results , say you don't know "
    "Instead of guessing."
)


def check_api_keys() -> None:
    """Stop early with a clear message if a required API key is missing."""
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY. Please add it to your .env file.")
    if not JINA_API_KEY:
        raise ValueError("Missing JINA_API_KEY. Please add it to your .env file.")