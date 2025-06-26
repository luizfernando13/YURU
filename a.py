import base64
import msgpack
from Crypto.Cipher import AES
import lz4.frame

# Pegue o payload EXATO do request/resposta:
payload = "0fd9e670be97abfea02b9fc08c7a68f9enq996jN+3yXnKYQpycc+3cAYVqlwGs2zAXpPMQ+1qs="

# Separe a parte HEX do resto
hex_prefix = payload[:32] # 32 caracteres hex = 16 bytes
b64_suffix = payload[32:]

iv = bytes.fromhex(hex_prefix)
ciphertext = base64.b64decode(b64_suffix)

# Sua key AES
key = bytes.fromhex("2f22172f31657bf41b835b6372a6221d")

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)
print("Primeiros 64 bytes descriptografados:", decrypted[:64])
try:
    decompressed = lz4.frame.decompress(decrypted)
    print("Decompress OK, tentando MessagePack…")
    unpacked = msgpack.unpackb(decompressed)
    print("Decoded (LZ4 + MessagePack):", unpacked)
except Exception as e:
    print("Nem LZ4 nem msgpack direto:", e)
