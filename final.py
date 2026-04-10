from fastapi import FastAPI
from pydantic import BaseModel
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

#  Load env variables
load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
VAULT_URL = os.getenv("KEY_VAULT_URL")

#  Authenticate
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

client = SecretClient(vault_url=VAULT_URL, credential=credential)

#  FastAPI app
app = FastAPI()

# Request model
class KeyValue(BaseModel):
    key: str
    value: str

#  Store secret in Key Vault
@app.post("/store-secret")
def store_secret(data: KeyValue):
    client.set_secret(data.key, data.value)
    return {"message": f" Secret '{data.key}' stored successfully"}

#  Get secret from Key Vault
@app.get("/get-secret/{key}")
def get_secret(key: str):
    try:
        secret = client.get_secret(key)
        return {"key": key, "value": secret.value}
    except Exception:
        return {"error": f" Secret '{key}' not found"}