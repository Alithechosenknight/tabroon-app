from cryptography.hazmat.primitives import serialization

with open("test_key.pem", "rb") as f:
    key_data = f.read()
    try:
        private_key = serialization.load_pem_private_key(key_data, password=None)
        print("PEM key is valid!")
    except Exception as e:
        print("PEM key is INVALID:", e)