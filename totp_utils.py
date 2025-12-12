import base64
import binascii
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """Convert 64-char hex seed → Base32 string"""
    seed_bytes = binascii.unhexlify(hex_seed)   # hex → bytes
    base32_seed = base64.b32encode(seed_bytes)  # bytes → base32 bytes
    return base32_seed.decode()                 # convert to string


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)  # SHA-1, 30s period, 6 digits default
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a 6-digit TOTP code with ±30s time tolerance
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)
if __name__ == "__main__":
    # Read the seed from data/seed.txt
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    # Generate TOTP
    code = generate_totp_code(hex_seed)
    print(f"Generated TOTP: {code}")

    # Verify the same TOTP (should be true)
    print("Verification:", verify_totp_code(hex_seed, code))
