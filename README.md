# Spring Boot Generator API

A REST API service that generates Spring Boot projects with AI-powered code generation using Azure OpenAI.

## Features

- 🚀 **AI-Powered Code Generation** - Uses Azure OpenAI to generate Spring Boot components
- 🔧 **Configurable Features** - Database, Security, Messaging, AWS, Monitoring, etc.
- 📦 **ZIP Download** - Generates complete project structure as downloadable ZIP
- 🌐 **REST API** - Clean REST endpoints for integration with any UI framework
- ⚡ **Azure Ready** - Optimized for Azure App Service deployment

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and usage guide |
| `/health` | GET | Health check for monitoring |
| `/generate` | POST | Generate Spring Boot project |

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd springboot_generator_genAI
```

2. **Set up environment variables**
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your Azure OpenAI credentials
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
# Development mode
python app.py

# Production mode
python startup.py
```

## Azure Deployment

### Prerequisites
- Azure subscription
- Azure OpenAI service configured
- GitHub repository

### Deploy to Azure App Service

1. **Create Azure App Service**
   - Runtime: Python 3.11
   - Operating System: Linux
   - Region: Your preferred region

2. **Configure Environment Variables in Azure**
   Go to App Service → Configuration → Application Settings:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_KEY=your-api-key
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   ```

3. **Set up GitHub Deployment**
   - Go to App Service → Deployment Center
   - Select GitHub as source
   - Choose your repository and branch
   - Azure will automatically deploy on git push

### Azure CLI Deployment (Alternative)

```bash
# Login to Azure
az login

# Create resource group
az group create --name springboot-api-rg --location "East US"

# Create App Service plan
az appservice plan create --name api-plan --resource-group springboot-api-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group springboot-api-rg --plan api-plan --name your-unique-api-name --runtime "PYTHON|3.11"

# Configure environment variables
az webapp config appsettings set --resource-group springboot-api-rg --name your-unique-api-name --settings \
  AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
  AZURE_OPENAI_KEY="your-api-key" \
  AZURE_OPENAI_DEPLOYMENT="your-deployment-name"

# Deploy from GitHub
az webapp deployment source config --resource-group springboot-api-rg --name your-unique-api-name --repo-url https://github.com/yourusername/your-repo --branch main
```

## API Usage Examples

### Generate Spring Boot Project

**Request:**
```bash
curl -X POST https://your-app-name.azurewebsites.net/generate \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "MySpringApp",
    "groupId": "com.example.demo",
    "database": true,
    "security": true,
    "messaging": true,
    "aws": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Spring Boot project generated successfully",
  "project_name": "MySpringApp", 
  "zip_file": "MySpringApp.zip"
}
```

### Health Check
```bash
curl https://your-app-name.azurewebsites.net/health
```

## Supported Features

- `database` - Database configuration and JPA setup
- `security` - Spring Security with JWT
- `messaging` - Message listeners and queue configuration
- `streaming` - Kafka integration
- `aws` - AWS S3 configuration
- `monitoring` - Actuator and Prometheus
- `logging` - Logging configuration
- `containerization` - Docker files

## Production Considerations

1. **CORS Configuration**: Update CORS origins in `app.py` for your specific UI domains
2. **Environment Variables**: Never commit `.env` file to repository
3. **Monitoring**: Use Azure Application Insights for monitoring
4. **Scaling**: Configure auto-scaling rules in Azure App Service

## Project Structure

```
├── app.py                 # Main Flask application
├── startup.py            # Production entry point
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version for Azure
├── web.config           # Azure App Service configuration
├── env.example          # Environment variables template
├── generator/           # Code generation modules
│   ├── ai_generator.py  # Azure OpenAI integration
│   ├── template_manager.py
│   ├── file_writer.py
│   └── freemarker_generator.py
└── templates/           # Project templates
```

## License

[Your License Here] 