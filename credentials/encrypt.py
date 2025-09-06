# username and password encrypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def loginEncrypt(message):
    key = "u2oh6Vu^HWe4_AES"
    key_bytes = key.encode('utf-8')
    iv = key_bytes
    message_bytes = message.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypted_message = cipher.encrypt(pad(message_bytes, AES.block_size))
    encrypted_message_b64 = base64.b64encode(encrypted_message).decode('utf-8')
    return encrypted_message_b64