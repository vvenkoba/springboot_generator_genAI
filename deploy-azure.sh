#!/bin/bash

# Azure CLI deployment script for Spring Boot Generator API
# Run this after: az login

# Configuration
RESOURCE_GROUP="springboot-api-rg"
APP_NAME="your-unique-api-name"  # Change this to your desired name
LOCATION="eastus"
GITHUB_REPO="https://github.com/yourusername/your-repo-name"  # Update with your repo URL

echo "Creating Azure App Service for Spring Boot Generator API..."

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
echo "Creating App Service plan..."
az appservice plan create \
  --name "${APP_NAME}-plan" \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create web app
echo "Creating Web App..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan "${APP_NAME}-plan" \
  --name $APP_NAME \
  --runtime "PYTHON|3.11"

# Configure environment variables
echo "Setting environment variables..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://kafka-migration.openai.azure.com/" \
    AZURE_OPENAI_KEY="38kZiRMs4ykHlrd8RHLfTRzPI87qWgdn11KkCnEeIX8QOa6Ew3rbJQQJ99BEACYeBjFXJ3w3AAABACOGRN3v" \
    AZURE_OPENAI_DEPLOYMENT="gpt-4.1"

# Configure GitHub deployment (requires GitHub authorization)
echo "Setting up GitHub deployment..."
az webapp deployment source config \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --repo-url $GITHUB_REPO \
  --branch main \
  --manual-integration

echo "✅ Deployment complete!"
echo "Your API will be available at: https://${APP_NAME}.azurewebsites.net"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Test your API endpoints"
echo "3. Update CORS settings in app.py for production" 