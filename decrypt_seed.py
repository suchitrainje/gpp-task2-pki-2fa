#!/usr/bin/env python3
# decrypt_seed.py
import base64
import os
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidKey, InvalidSignature

KEY_PATH = "keys/student_private.pem"
ENCRYPTED_FILE = "encrypted_seed.txt"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "seed.txt")

HEX_CHARS = set("0123456789abcdef")

def load_private_key(path: str):
    with open(path, "rb") as f:
        key_bytes = f.read()
    try:
        key = serialization.load_pem_private_key(key_bytes, password=None)
    except Exception as e:
        raise RuntimeError(f"Failed to load private key: {e}")
    return key

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP-SHA256
    Returns a 64-character lowercase hex string on success.
    Raises RuntimeError on failure.
    """
    try:
        ct = base64.b64decode(encrypted_seed_b64)
    except Exception as e:
        raise RuntimeError(f"Base64 decode failed: {e}")

    try:
        plain = private_key.decrypt(
            ct,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"RSA decryption failed: {e}")

    try:
        seed = plain.decode("utf-8").strip()
    except Exception as e:
        raise RuntimeError(f"Failed to decode plaintext as UTF-8: {e}")

    # Validate: 64 chars, hex lowercase
    if len(seed) != 64:
        raise RuntimeError(f"Invalid seed length: expected 64 chars, got {len(seed)}")

    if any(ch not in HEX_CHARS for ch in seed):
        raise RuntimeError("Invalid seed characters: seed must be lowercase hex 0-9a-f")

    return seed

def main():
    if not os.path.exists(ENCRYPTED_FILE):
        print(f"ERROR: {ENCRYPTED_FILE} not found in repo root. Run Step 4 first.", file=sys.stderr)
        sys.exit(2)

    # Load private key
    try:
        priv = load_private_key(KEY_PATH)
    except RuntimeError as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(3)

    # Read encrypted seed file
    enc_text = open(ENCRYPTED_FILE, "r").read().strip()

    try:
        seed_hex = decrypt_seed(enc_text, priv)
    except RuntimeError as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(4)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write seed to data/seed.txt with safe permissions
    with open(OUTPUT_FILE, "w") as f:
        f.write(seed_hex + "\n")

    try:
        # chmod 600 if running on *nix; on Windows this will silently fail but we ignore
        os.chmod(OUTPUT_FILE, 0o600)
    except Exception:
        pass

    print("OK: Decrypted seed saved to", OUTPUT_FILE)
    print("Seed preview (first 8 chars):", seed_hex[:8])

if __name__ == "__main__":
    main()
