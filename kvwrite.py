from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import ResourceManagementClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

# 🔹 Hardcoded access control
user_access = {
    "userA": ["jatinkvs"],     # can write only here
    "userB": ["test-one"],     # can write only here
    "userC": []                # read-only
}

# 🔹 Request model
class SecretRequest(BaseModel):
    vault_name: str
    key: str
    value: str


# 🔹 Get all vaults (OPEN for all users)
@app.get("/vaults")
def list_vaults():

    credential = AzureCliCredential()
    client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

    vaults = []

    for resource in client.resources.list(
        filter="resourceType eq 'Microsoft.KeyVault/vaults'"
    ):
        vaults.append(resource.name)

    return {"vaults": vaults}


# 🔹 Create Key Vault client
def get_kv_client(vault_name):
    credential = AzureCliCredential()
    vault_url = f"https://{vault_name}.vault.azure.net/"
    return SecretClient(vault_url=vault_url, credential=credential)


# 🔹 Store secret (RESTRICTED)
@app.post("/store-secret")
def store_secret(data: SecretRequest, user: str = Header(...)):

    allowed_vaults = user_access.get(user, [])

    # 🔥 Access check
    if data.vault_name not in allowed_vaults:
        raise HTTPException(status_code=403, detail="❌ No write access to this vault")

    client = get_kv_client(data.vault_name)
    client.set_secret(data.key, data.value)

    return {
        "message": f"✅ Secret stored in {data.vault_name} by {user}"
    }


# 🔹 Root
@app.get("/")
def home():
    return {"message": "🚀 Vault Access API Running"}