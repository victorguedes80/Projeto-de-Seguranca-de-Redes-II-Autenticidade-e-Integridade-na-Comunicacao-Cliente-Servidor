import json

with open("captured_packet.json") as f:
    packet = json.load(f)

print("\n[ATACANTE PASSIVO]")
print("Conteúdo capturado:")
print(packet["data"])
