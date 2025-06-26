import re

ARQUIVO = "dump.cs"        # ou o arquivo C# que quiser
LOGFILE = "crypto_cs_log.txt"

chaves = [
    "Encrypt", "Decrypt", "Crypt", "Cipher", "Xor", "Obfuscate", "Encode", "Decode",
    "Aes", "Rijndael", "ICryptoTransform", "System.Security.Cryptography", "ToBase64", "FromBase64",
    "AesCryptoServiceProvider", "RijndaelManaged", "MessagePack", "LZ4", "Compress", "Decompress",
    "RSACryptoServiceProvider", "PKCS7", "CBC", "IV", "Key", "key", "public", "private"
]

def busca_crypto_cs(filename, palavras, logfile):
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    with open(logfile, "w", encoding="utf-8") as log:
        log.write(f"🔎 Crypto finder log para arquivo {filename}\n\n")
        for chave in palavras:
            achou = False
            for m in re.finditer(chave, text, re.IGNORECASE):
                achou = True
                # Pega algumas linhas antes e depois para contexto
                linha = text.count('\n', 0, m.start())
                linhas = text.split('\n')
                ini = max(0, linha-5)
                fim = min(len(linhas), linha+10)
                snippet = "\n".join(linhas[ini:fim])
                header = f"\n=== [ {chave} ] (linha {linha+1}) ===\n"
                footer = "-"*60 + "\n"
                print(header + snippet + "\n" + footer)
                log.write(header + snippet + "\n" + footer)
            if not achou:
                msg = f"Nenhum resultado para {chave}\n"
                print(msg)
                log.write(msg)
        log.write("\n✅ Busca finalizada.\n")
    print(f"\nArquivo de log salvo como: {logfile}")

busca_crypto_cs(ARQUIVO, chaves, LOGFILE)
