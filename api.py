from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
from decrypt_seed import decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code
import time

app = FastAPI()

SEED_FILE = "data/seed.txt"

# Root endpoint
@app.get("/")
def home():
    return {"message": "2FA service running"}


# ------------ Request Models ------------
class EncryptedSeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# ------------ 1. POST /decrypt-seed ------------
@app.post("/decrypt-seed")
def decrypt_seed_api(req: EncryptedSeedRequest):
    try:
        from cryptography.hazmat.primitives import serialization

        with open("keys/student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
            )

        hex_seed = decrypt_seed(req.encrypted_seed, private_key)

        if len(hex_seed) != 64:
            raise ValueError("Invalid decrypted seed")

        os.makedirs("data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        print("Decryption error:", e)
        raise HTTPException(status_code=500, detail="Decryption failed")


# ------------ 2. GET /generate-2fa ------------
@app.get("/generate-2fa")
def generate_2fa():
    try:
        if not os.path.exists(SEED_FILE):
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")

        seed = open(SEED_FILE).read().strip()
        code = generate_totp_code(seed)
        valid_for = 30 - (int(time.time()) % 30)

        return {"code": code, "valid_for": valid_for}

    except Exception as e:
        print("TOTP error:", e)
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")


# ------------ 3. POST /verify-2fa ------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    try:
        seed = open(SEED_FILE).read().strip()
        is_valid = verify_totp_code(seed, req.code)
        return {"valid": is_valid}

    except Exception as e:
        print("Verification error:", e)
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
