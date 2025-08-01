import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-12-01-preview"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_code(file_type: str, spec: dict) -> str:
    prompt = f"""
You are an expert Spring Boot code generator.
Create the full {file_type} for the following project:
{json.dumps(spec, indent=2)}
ONLY RETURN THE RAW CODE.
"""
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message["content"]