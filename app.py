from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from generator.ai_generator import generate_code
from generator.template_manager import render_template
from generator.file_writer import write_generated_file
import shutil, zipfile
import logging
import os

app = Flask(__name__)

# Enable CORS for all routes to allow UI applications to call this API
# TODO: In production, replace "*" with your specific UI domain(s)
# Example: CORS(app, origins=["https://your-ui-app.azurewebsites.net", "https://your-custom-domain.com"])
CORS(app, origins=["*"])  # Allow all origins for development/testing

# Configure logging for production
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "generated_output"
TEMPLATE_DIR = BASE_DIR / "templates"

FEATURE_FILE_MAP = {
    "database": ["DatabaseConfig.java"],
    "messaging": ["MessageListener.java"],
    "streaming": ["KafkaConfig.java", "KafkaConsumer.java"],
    "containerization": ["Dockerfile", "docker-compose.yml"],
    "repository": ["GitConfig.java", "CiPipeline.yml"],
    "security": ["SecurityConfig.java", "JwtUtils.java"],
    "logging": ["LoggingConfig.java"],
    "aws": ["S3Config.java"],
    "scanning": ["CodeQualityReport.md"],
    "monitoring": ["ActuatorConfig.java", "PrometheusConfig.java"]
}

PACKAGE_MAP = {
    "Entity.java": "entity",
    "Model.java": "model",
    "Repository.java": "repository",
    "Service.java": "service",
    "Controller.java": "controller",
    "DatabaseConfig.java": "config",
    "KafkaConfig.java": "config",
    "KafkaConsumer.java": "config",
    "SecurityConfig.java": "config",
    "JwtUtils.java": "config",
    "S3Config.java": "config",
    "LoggingConfig.java": "config",
    "ActuatorConfig.java": "config",
    "PrometheusConfig.java": "config",
    "GitConfig.java": "config"
}

CORE_COMPONENTS = ["Entity", "Model", "Repository", "Service", "Controller"]

# Health check endpoint for Azure App Service monitoring
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring service status"""
    return jsonify({"status": "healthy", "service": "springboot-generator-api"}), 200

# API information endpoint
@app.route("/", methods=["GET"])
@app.route("/api/info", methods=["GET"])
def api_info():
    """API information and usage guide"""
    return jsonify({
        "service": "Spring Boot Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/generate": {
                "method": "POST",
                "description": "Generate Spring Boot project with specified features",
                "content-type": "application/json"
            },
            "/health": {
                "method": "GET", 
                "description": "Health check endpoint"
            }
        },
        "example_request": {
            "projectName": "MyProject",
            "groupId": "com.example",
            "database": True,
            "security": True,
            "messaging": True
        }
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON", "status": "error"}), 400
        
        spec = request.get_json()
        if not spec:
            return jsonify({"error": "Empty request body", "status": "error"}), 400
        
        # Validate required fields
        if "groupId" not in spec:
            return jsonify({"error": "Missing required field: groupId", "status": "error"}), 400
        
        app.logger.info(f"Generating project with spec: {spec}")
        
        project_name = spec.get("projectName", "demo").replace(" ", "-")
        base_package = Path(*spec["groupId"].split("."))
        target_dir = OUTPUT_DIR / project_name
        main_java_dir = target_dir / "src/main/java" / base_package
        test_java_dir = target_dir / "src/test/java" / base_package
        target_dir.mkdir(parents=True, exist_ok=True)

        static_files = [c + ".java" for c in CORE_COMPONENTS] + ["pom.xml"]
        dynamic_files = set()

        for feature, files in FEATURE_FILE_MAP.items():
            if feature in spec:
                dynamic_files.update(files)

        # Add test files for all components
        for comp in CORE_COMPONENTS:
            dynamic_files.add(f"{comp}Test.java")

        all_files = static_files + list(dynamic_files)

        for file_type in all_files:
            try:
                code = generate_code(file_type, spec)
            except Exception:
                code = render_template(TEMPLATE_DIR, file_type, spec)

            if file_type.endswith(".java"):
                class_name = file_type.replace(".java", "")
                is_test = "Test" in class_name
                base_name = class_name.replace("Test", "")
                subpkg = PACKAGE_MAP.get(f"{base_name}.java", "config")
                java_path = (test_java_dir if is_test else main_java_dir) / subpkg / file_type
            else:
                java_path = target_dir / file_type

            write_generated_file(java_path, code)

        zip_path = OUTPUT_DIR / f"{project_name}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in target_dir.rglob("*"):
                zipf.write(file, file.relative_to(target_dir))

        app.logger.info(f"Successfully generated project: {project_name}")
        return jsonify({
            "status": "success", 
            "message": "Spring Boot project generated successfully",
            "project_name": project_name,
            "zip_file": f"{project_name}.zip"
        }), 200
        
    except KeyError as e:
        app.logger.error(f"Missing required field: {e}")
        return jsonify({"error": f"Missing required field: {e}", "status": "error"}), 400
    except Exception as e:
        app.logger.error(f"Error generating project: {str(e)}")
        return jsonify({"error": "Internal server error while generating project", "status": "error"}), 500

if __name__ == "__main__":
    # For local development
    app.run(debug=True, host="0.0.0.0", port=5000)