import socket, time, os, json
from cryptography.hazmat.primitives import serialization
from crypto_utils import sign_data, send_packet

with open("keys/client_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), None)

msg = input("Mensagem: ")

data = {
    "message": msg,
    "timestamp": time.time(),
    "nonce": os.urandom(8).hex()
}

signature = sign_data(data, private_key)

packet = {
    "data": data,
    "signature": signature.hex()
}

# Simula captura na rede
with open("captured_packet.json", "w") as f:
    json.dump(packet, f)

s = socket.socket()
s.connect(("localhost", 7777))
send_packet(s, packet)
s.close()

print("[ok] Mensagem enviada")
