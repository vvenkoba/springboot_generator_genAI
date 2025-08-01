from .ai_generator import generate_code
import os, json

def generate_template(ftl_path: str, file_type: str, spec: dict):
    if not os.path.exists(ftl_path):
        print(f"Creating missing template: {ftl_path}")
        prompt = f"""
Generate a Freemarker (.ftl) template for a {file_type} in a Spring Boot application based on the following spec:
{json.dumps(spec, indent=2)}
Only return template code.
"""
        code = generate_code(file_type + " Freemarker template", spec)
        with open(ftl_path, "w") as f:
            f.write(code)