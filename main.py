import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def get_code_content(filename):
  """
  Reads the content of the code file.
  """
  with open(filename, "r") as f:
    return f.read()
  
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY");

MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4"
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=MODEL)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are senior front end engineer.\
     You are an expert in React, Material UI and Typescript. You prefer using Styled Components.\
     I will provide you with current version of code which I am working on.\
     I will give you instructions and you will help me modify the code accordingly.\
     "),
    ("user", "{input}")
])

chain = prompt_template | llm 

filename = "/Users/drodi/repos/lastseenweb/src/pages/HowItWorks.tsx"

while True:
   code_content = get_code_content(filename)
   command = input("Ask a question about code: ")
   if command == "exit":
     break
   prompt = f"Current Code:\n{code_content}\n\nInstructions: {command}\n"


   # Run the chat completion with the formatted prompt
   response = chain.invoke({"input": prompt})

   # Print the AI's response in yellow
   print(f"\033[93m{response.content}\033[0m")
