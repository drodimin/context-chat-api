from config import MODEL_MAP, OPENAI_API_KEY
from langchain_openai import ChatOpenAI

def get_code_content(filename):
    with open(filename, "r") as f:
        return f.read()

def change_model(model_number):
    if model_number in MODEL_MAP:
        new_model = MODEL_MAP[model_number]
        llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=new_model)  # Create a new ChatOpenAI instance with the new model
        print(f"Model changed to {new_model}")
        return llm
    else:
        print("Invalid model number. No changes made.")
        return None
