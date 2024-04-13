from enum import Enum
import json
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_caching import Cache
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from diff import extract_modified_code
from test_diff_processor import load_file_content


class Models(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
cache = Cache(app)

CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:3001"]}})

# Create a Blueprint for API routes
api_blueprint = Blueprint('api', __name__)

# Initialize the LLM with a default model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=Models.GPT_3_5_TURBO.value)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "1. Role: Senior front-end engineer with expertise in React, Material UI, TypeScript, and MUI Styled Components.\
                2. Task: Analyze and modify the provided code based on instructions.\
                3. Response: Return the modified code in one snippet\
     "),
    ("user", "{input}")
])

chain = prompt_template | llm


@api_blueprint.route('/process_command', methods=['POST'])
@cache.cached(timeout=600, query_string=True) 
def process_command():
    data = request.json
    model = data.get('model')
    command = data.get('command')
    context = data.get('context')

    if llm.model_name != model:
        llm.model_name = model
        print(f"Model changed to {model}")

    prompt = f"Current Code:\n{context}\n\nInstructions: {command}\n"
    response = chain.invoke({"input": prompt})
    modified_code = extract_modified_code(response.content)

    print(prompt)
    print(response.content)

    return jsonify({"modified_code": modified_code}), 200


@api_blueprint.route('/diff_test', methods=['POST'])
@cache.cached(timeout=600, query_string=True) 
def diff_test():
    original_file_path = 'test/original.txt'
    modified_file_path = 'test/modified.txt'

    # Load the content of the original and modified files
    original_content = load_file_content(original_file_path)
    modified_content = load_file_content(modified_file_path)

    return jsonify({"modified_code": modified_content}), 200

app.register_blueprint(api_blueprint, url_prefix='/api')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
