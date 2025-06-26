import re

ARQUIVO = "dump.cs"          # Altere para o seu arquivo
LOGFILE = "referencias_log.txt"

palavras = [
    "Aes256", "EncryptoBody", "DecryptoBody", "Build", "HttpClientBuilder", "WebRequestClient"
]

def busca_referencias(filename, palavras, logfile, contexto=6):
    with open(filename, encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()
    
    with open(logfile, "w", encoding="utf-8") as log:
        log.write(f"🔎 Referências customizadas para arquivo {filename}\n\n")
        for palavra in palavras:
            encontrados = 0
            print(f"\n=== [ {palavra} ] ===")
            log.write(f"\n=== [ {palavra} ] ===\n")
            for idx, linha in enumerate(linhas):
                if re.search(rf'\b{re.escape(palavra)}\b', linha, re.IGNORECASE):
                    encontrados += 1
                    start = max(0, idx - contexto)
                    end = min(len(linhas), idx + contexto + 1)
                    snippet = "".join(linhas[start:end])
                    header = f"\n[linha {idx+1}]\n"
                    footer = "-"*60 + "\n"
                    print(header + snippet + footer)
                    log.write(header + snippet + footer)
            if not encontrados:
                msg = f"Nenhuma referência encontrada para {palavra}\n"
                print(msg)
                log.write(msg)
        log.write("\n✅ Busca finalizada.\n")
    print(f"\nArquivo de log salvo como: {logfile}")

busca_referencias(ARQUIVO, palavras, LOGFILE)
