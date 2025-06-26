import base64
from Crypto.Cipher import AES
import msgpack
import lz4.frame
import msgpack

hex_prefix = "e798d9db2fcaa840beeb6759a1021876"
b64_suffix = "DCYOzNUMvJZb8TafwgaVRzN+FKp2cQ4wvkuDnDkZAqQL9PkGTQv190V74iV045hNOPhImi/fsx3ED1J2HsxioQ=="

iv = bytes.fromhex(hex_prefix)
ciphertext = base64.b64decode(b64_suffix)
print("Tamanho do ciphertext:", len(ciphertext))
print("Restante % 16:", len(ciphertext) % 16)

key = bytes.fromhex("2f22172f31657bf41b835b6372a6221d")

# Garante bloco múltiplo de 16 para teste (NÃO IDEAL, só pra debug):
while len(ciphertext) % 16 != 0:
    ciphertext += b"\x00"

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)
print("Primeiros 64 bytes descriptografados:", decrypted)
print("Primeiros 64 bytes descriptografados (hex):", decrypted[:64].hex())
try:
    decompressed = lz4.frame.decompress(decrypted)
    unpacked = msgpack.unpackb(decompressed, raw=False)
    print("LZ4 + Msgpack OK:", unpacked)
except Exception as e:
    print("Falhou LZ4/Msgpack:", e)

try:
    unpacked = msgpack.unpackb(decrypted, raw=False)
    print("Decoded:", unpacked)
except Exception as e:
    print("Falhou msgpack:", e)
    
for i in range(0, 16):
    try:
        obj = msgpack.unpackb(decrypted[i:], raw=False)
        print(f"Msgpack OK no offset {i}: {obj}")
        break
    except Exception as e:
        print(f"Offset {i}: {e}")