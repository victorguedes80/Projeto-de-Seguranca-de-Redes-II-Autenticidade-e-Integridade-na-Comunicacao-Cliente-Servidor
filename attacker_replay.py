import socket, json
from crypto_utils import send_packet

with open("captured_packet.json") as f:
    packet = json.load(f)

print("[ATACANTE DE REPLAY] Reenviando pacote capturado")

s = socket.socket()
s.connect(("localhost", 7777))
send_packet(s, packet)
s.close()
