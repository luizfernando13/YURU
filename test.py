import re

ARQUIVO = "global-metadata.dat"
LOGFILE = "crypto_search_log.txt"

chaves = [
    "Encrypt", "Decrypt", "Crypt", "Cipher", "Xor", "Obfuscate", "Encode", "Decode",
    "Aes", "Rijndael", "ICryptoTransform", "System.Security.Cryptography", "ToBase64", "FromBase64", "AesCryptoServiceProvider", "RijndaelManaged"
]

def busca_crypto(filename, palavras, logfile):
    with open(filename, "rb") as f:
        data = f.read()

    try:
        text = data.decode("utf-8", errors="ignore")
    except:
        text = str(data)
    
    with open(logfile, "w", encoding="utf-8") as log:
        log.write(f"🔎 Crypto finder log para arquivo {filename}\n\n")
        for chave in palavras:
            achou = False
            for m in re.finditer(chave, text, re.IGNORECASE):
                achou = True
                start = max(0, m.start()-60)
                end = min(len(text), m.end()+120)
                snippet = text[start:end]
                header = f"\n=== [ {chave} ] ===\n"
                footer = "-"*60 + "\n"
                print(header + snippet + "\n" + footer)
                log.write(header + snippet + "\n" + footer)
            if not achou:
                msg = f"Nenhum resultado para {chave}\n"
                print(msg)
                log.write(msg)
        log.write("\n✅ Busca finalizada.\n")
    print(f"\nArquivo de log salvo como: {logfile}")

busca_crypto(ARQUIVO, chaves, LOGFILE)
