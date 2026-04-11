from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.keyvault import KeyVaultManagementClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

# Access control
user_access = {
    "userA": ["jatinkvs"],
    "userB": ["test-one"],
    "userC": []
}

#  Request model
class SecretRequest(BaseModel):
    vault_name: str
    key: str
    value: str


# List vaults (simpler)
@app.get("/vaults")
def list_vaults():
    credential = AzureCliCredential()
    client = KeyVaultManagementClient(credential, SUBSCRIPTION_ID)

    vaults = []

    #  No filter, direct listing
    for kv in client.vaults.list():
        vaults.append(kv.name)

    return {"vaults": vaults}


#  Key Vault client
def get_kv_client(vault_name):
    credential = AzureCliCredential()
    vault_url = f"https://{vault_name}.vault.azure.net/"
    return SecretClient(vault_url=vault_url, credential=credential)


# Store secret (restricted)
@app.post("/store-secret")
def store_secret(data: SecretRequest, user: str = Header(...)):

    allowed_vaults = user_access.get(user, [])

    if data.vault_name not in allowed_vaults:
        raise HTTPException(status_code=403, detail="❌ No write access")

    client = get_kv_client(data.vault_name)
    client.set_secret(data.key, data.value)

    return {"message": f"✅ Stored in {data.vault_name}"}
