from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

key = Fernet.generate_key()
cipher = Fernet(key)

class SeedRequest(BaseModel):
    seed: str

class EncryptedSeedRequest(BaseModel):
    encrypted_seed: str

@app.post("/encrypt-seed")
def encrypt_seed(data: SeedRequest):
    encrypted = cipher.encrypt(data.seed.encode())
    return {"encrypted_seed": encrypted.decode()}

@app.post("/decrypt-seed")
def decrypt_seed(data: EncryptedSeedRequest):
    decrypted = cipher.decrypt(data.encrypted_seed.encode())
    return {"seed": decrypted.decode()}
