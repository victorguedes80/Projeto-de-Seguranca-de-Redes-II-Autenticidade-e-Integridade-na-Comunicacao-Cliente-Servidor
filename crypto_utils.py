import struct
import json
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def send_packet(sock, data_dict):
    """Envia dicionário como JSON com cabeçalho de tamanho."""
    serialized = json.dumps(data_dict).encode('utf-8')
    sock.sendall(struct.pack('>I', len(serialized)) + serialized)

def recv_packet(sock):
    """Recebe pacote JSON com tamanho prefixado."""
    raw_len = _recv_exact(sock, 4)
    if not raw_len: return None
    msg_len = struct.unpack('>I', raw_len)[0]
    raw_msg = _recv_exact(sock, msg_len)
    return json.loads(raw_msg) if raw_msg else None

def _recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data += packet
    return data

#RSA-PSS

def sign_data(data_dict, private_key):
    """Gera assinatura digital para o dicionário."""
    # sort_keys=True é CRUCIAL para garantir a mesma ordem dos bytes
    payload = json.dumps(data_dict, sort_keys=True).encode('utf-8')
    return private_key.sign(
        payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def verify_signature_data(data_dict, signature_hex, public_key):
    """Verifica se os dados correspondem à assinatura."""
    try:
        payload = json.dumps(data_dict, sort_keys=True).encode('utf-8')
        signature = bytes.fromhex(signature_hex)
        public_key.verify(
            signature,
            payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except:
        return False