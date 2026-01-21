import socket
import time
from cryptography.hazmat.primitives import serialization
from crypto_utils import recv_packet, verify_signature_data

# Configuração
PORT = 7777
WINDOW_SECONDS = 60
USE_NONCE_CHECK = True  # toggle para demonstrar antes/depois

# Carregar chave pública
with open("keys/client_public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Estrutura anti-replay por nonce (expiração simples)
seen_nonces = {}  # nonce -> timestamp

def cleanup_nonces():
    now = time.time()
    to_delete = [n for n,t in seen_nonces.items() if now - t > WINDOW_SECONDS]
    for n in to_delete:
        del seen_nonces[n]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", PORT))
s.listen(1)

print("\n" + "="*40)
print("    SERVIDOR DE AUTENTICIDADE ATIVO")
print("="*40)

while True:
    conn, addr = s.accept()
    packet = recv_packet(conn)

    if packet:
        data = packet.get('data', {})
        signature_hex = packet.get('signature', '')
        print(f"\n{'='*10} NOVA MENSAGEM RECEBIDA {'='*10}")
        print(f"Origem: {addr}")
        print(f"Conteúdo: {data.get('message')}")

        # 1. Verificação Criptográfica (Integridade e Autoria)
        is_signature_valid = verify_signature_data(data, signature_hex, public_key)

        # 2. Verificação Temporal (Anti-Replay) - Janela de WINDOW_SECONDS
        try:
            msg_time = float(data.get('timestamp', 0))
        except Exception:
            msg_time = 0.0
        now = time.time()
        is_time_valid = (0 <= now - msg_time < WINDOW_SECONDS)  # rejeita timestamps futuros e muito antigos

        # 3. Verificação de nonce (se ativado)
        nonce = data.get('nonce')
        nonce_ok = True
        if USE_NONCE_CHECK:
            cleanup_nonces()
            if not nonce:
                nonce_ok = False
            elif nonce in seen_nonces:
                nonce_ok = False
            else:
                # registra nonce com timestamp da mensagem
                seen_nonces[nonce] = msg_time

        print("-" * 40)
        print("RESULTADO DA ANÁLISE:")

        if is_signature_valid and is_time_valid and nonce_ok:
            print("AUTENTICIDADE: CONFIRMADA")
            print("INTEGRIDADE:   PRESERVADA")
            print("TEMPORALIDADE: VÁLIDA")
            print("NONCE:         OK")
            print("\n>> MENSAGEM ACEITA <<")

        else:
            print(" ALERTA DE SEGURANÇA DETECTADO ")
            if not is_signature_valid:
                print("   -> FALHA: A assinatura não corresponde aos dados (Dados alterados?)")
            if not is_time_valid:
                print("   -> FALHA: Timestamp inválido/expirado (Possível replay)")
            if not nonce_ok:
                print("   -> FALHA: Nonce inválido ou reutilizado (Replay detectado)")
            print("\n>> MENSAGEM DESCARTADA <<")

    conn.close()
