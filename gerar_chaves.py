from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048 #Tamanho do módulo RSA
)

private_key = key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

public_key = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

open("keys/client_private.pem", "wb").write(private_key)
open("keys/client_public.pem", "wb").write(public_key)

print("Chaves geradas com sucesso!")
