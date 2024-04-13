import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_MAP = {
    "3": "gpt-3.5-turbo",
    "4": "gpt-4",
    # Add more mappings here as needed
}

FILE_NAME = os.getenv("FILE_NAME")