from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os
load_dotenv()

# 🔹 ENV VARIABLES (set before running)
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
VAULT_URL = os.getenv("KEY_VAULT_URL")

# 🔹 Authenticate using Service Principal
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# 🔹 Create client
client = SecretClient(vault_url=VAULT_URL, credential=credential)

# 🔹 Input (you can later take from user)
key = input("Enter key name: ")
value = input("Enter value: ")

# 🔹 Store secret in Key Vault
client.set_secret(key, value)

print(f"✅ Secret '{key}' stored successfully in Key Vault")