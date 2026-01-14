import hvac
import os

client = hvac.Client(
    url=os.getenv("VAULT_ADDR"),
    token=os.getenv("VAULT_TOKEN")
)

def get_gemini_key():
    secret = client.secrets.kv.read_secret_version(path="gemini")
    return secret["data"]["data"]["api_key"]
