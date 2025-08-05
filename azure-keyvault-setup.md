# Azure Key Vault Setup for Enhanced Security

## Why Use Azure Key Vault?
- 🔐 **Hardware Security Module (HSM)** backed
- 🔄 **Automatic key rotation**
- 📊 **Audit logging** for all access
- 🎯 **Fine-grained access control**
- 🛡️ **Azure AD integration**

## Setup Steps

### 1. Create Azure Key Vault
```bash
# Create Key Vault
az keyvault create \
  --name "springboot-keyvault" \
  --resource-group "springboot-api-rg" \
  --location "eastus"

# Add secrets
az keyvault secret set --vault-name "springboot-keyvault" --name "AZURE-OPENAI-ENDPOINT" --value "https://kafka-migration.openai.azure.com/"
az keyvault secret set --vault-name "springboot-keyvault" --name "AZURE-OPENAI-KEY" --value "your-key-here"
az keyvault secret set --vault-name "springboot-keyvault" --name "AZURE-OPENAI-DEPLOYMENT" --value "gpt-4.1"
```

### 2. Grant App Service Access
```bash
# Enable system-assigned managed identity for App Service
az webapp identity assign --resource-group "springboot-api-rg" --name "your-app-name"

# Grant access to Key Vault
az keyvault set-policy \
  --name "springboot-keyvault" \
  --object-id $(az webapp identity show --resource-group "springboot-api-rg" --name "your-app-name" --query principalId --output tsv) \
  --secret-permissions get
```

### 3. Update App Service Configuration
In Azure Portal → App Service → Configuration → Application Settings:
```
AZURE_OPENAI_ENDPOINT = @Microsoft.KeyVault(VaultName=springboot-keyvault;SecretName=AZURE-OPENAI-ENDPOINT)
AZURE_OPENAI_KEY = @Microsoft.KeyVault(VaultName=springboot-keyvault;SecretName=AZURE-OPENAI-KEY)
AZURE_OPENAI_DEPLOYMENT = @Microsoft.KeyVault(VaultName=springboot-keyvault;SecretName=AZURE-OPENAI-DEPLOYMENT)
```

## Benefits
- ✅ **Zero secrets in configuration**
- ✅ **Automatic secret rotation**
- ✅ **Audit trail for all access**
- ✅ **Role-based access control** 