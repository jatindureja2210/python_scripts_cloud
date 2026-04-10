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
secret_key = input("Enter serect key to get value")

# 🔹 Create client
client = SecretClient(vault_url=VAULT_URL, credential=credential)

value = client.get_secret(secret_key).value

print(f"Value of{secret_key} is {value}")

