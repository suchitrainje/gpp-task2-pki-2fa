import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23P31A0520"
GITHUB_REPO_URL = "https://github.com/suchitrainje/gpp-task2-pki-2fa"

# Paste your public key EXACTLY as awk printed it
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwsfNdTultEZsqE1i4YGP\nooiTRO5gLWAOuCm4qGepM36sycrcCtunfUTqCLjrR5vJnQkxYHq1mwi702k9sjSj\nKJjjzKQlGtAO9fxwbprMCg30MhW7dg5soWbBDXotiULyO3ONGeFGyK0iWxNdTl49\niX5E60OAWn0K+0G8LBvNPAjx+hBidLfQ9+Q2iEEBYuV0QxpWAvwZfy08dFfgWG45\nfpY52RTmJ4YU6pCdk+mXZ99wECE4fFQwDU1ZixOqnW7VJqAZyElljyp/PTgWnBZw\nRr9t3eAwWUv4zweQvnE/qgy/lusvlFpHrl1NrqVlcqTZuJ58bIOzIfeA30eUIDF7\ngnAnQs18set0fmvELxA+qDe/NDyB9W14FOOCMP2l0GbnLh4gRpVpJKkdLrB6onNh\nHeA3XkDnMot7L5+my6lhlNRmPkDbF9Pq0gYx4C2Mz96QjPEoeeXq46QzBtlV+C7k\nIFQfJBni//atgMg34pbwtLV8RRtyVNm/H0ufUzNyljCmjhA7f6Gp0R01oKUo3N+9\nWdw936EBSN94zERXnLLc0KltX5H5xwTQhh1RP2Yo2C+ev8ho+SHrN3roP/bYw4Kp\n84wI/a97gE4fvEh4XESUArFj15cgCyGBOqdVG6N29V33x+mQIUq2M7vaW0JX8qcW\nE67naywaJeBRikVSPj7ERNMCAwEAAQ==\n-----END PUBLIC KEY-----\n"""

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": PUBLIC_KEY
}

response = requests.post(API_URL, json=payload, timeout=20)

print("Status:", response.status_code)
print("Response:", response.json())

# Save encrypted seed
if "encrypted_seed" in response.json():
    with open("encrypted_seed.txt", "w") as f:
        f.write(response.json()["encrypted_seed"])
    print("\nEncrypted seed saved to encrypted_seed.txt")
else:
    print("\nERROR: No encrypted seed returned")
