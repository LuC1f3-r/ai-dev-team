import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(DATA_DIR / "chroma_db"))
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT", "8501"))

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

class Settings:
    ollama_base_url = OLLAMA_BASE_URL
    chroma_db_path = CHROMA_DB_PATH
    default_port = DEFAULT_PORT

    @classmethod
    def get_openai_model(cls, model_name: str = "gpt-4"):
        return f"openai/{model_name}"

    @classmethod
    def get_anthropic_model(cls, model_name: str = "claude-3-opus-20240229"):
        return f"anthropic/{model_name}"

    @classmethod
    def get_ollama_model(cls, model_name: str):
        return f"ollama/{model_name}"

settings = Settings()