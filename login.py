from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from dotenv import load_dotenv
from azure.mgmt.resource import ResourceManagementClient
import os
from azure.identity import AzureCliCredential

load_dotenv()

app = FastAPI()

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

@app.get("/vaults")
def list_key_vaults():

    credential = AzureCliCredential()

    client = KeyVaultManagementClient(credential, SUBSCRIPTION_ID)
    vaults = []

    #  This ALWAYS returns all Key Vaults
    for kv in client.vaults.list():
        
        vaults.append(kv.name)

    return {"vaults": vaults}


