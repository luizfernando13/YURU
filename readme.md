Decodificando Payloads WebGL (YURU)
Este repositório contém tudo necessário para analisar e decodificar payloads criptografados trafegando entre o front (WebGL Unity) e a API do jogo YURU.

Visão Geral
O jogo utiliza uma camada de transporte criptografada. O fluxo é o seguinte:

O payload original é serializado com MessagePack.

Opcionalmente, o resultado é comprimido usando LZ4.

O resultado é criptografado usando AES-256-CBC, com PKCS#7 padding.

Por fim, o binário criptografado é Base64-encoded antes de ser transmitido (via HTTP).

Todas essas informações e helpers estão documentadas e podem ser auditadas usando os dumps global-metadata.dat, il2cpp.h e dump.cs (produzidos com o Il2CppDumper).

Como extrair e analisar a estrutura de rede
Já incluso no repositório:

global-metadata.dat: Metadata Unity extraída do bundle WebGL.

il2cpp.h e dump.cs: Gerados usando o Il2CppDumper.

Para re-extrair se necessário (nao devera ser necessario, so usa se mt urgente!):

Descompacte o arquivo .data.br do Unity (brotli):

brotli -d 006944efc46bdffb3f9dd65bea250447.data.br -o game.data
Extraia o metadata com UnityPy:

python extract_metadata.py game.data global-metadata.dat
Rode o Il2CppDumper:

dotnet publish Il2CppDumper/Il2CppDumper.csproj -c Release -r linux-x64 -f net8.0 --self-contained false
./Il2CppDumper/Il2CppDumper/bin/Release/net8.0/linux-x64/publish/Il2CppDumper bb4ba1cdafcb1f267516bd187901b456.wasm global-metadata.dat dump
Os arquivos dump.cs e il2cpp.h são a base para entender toda a estrutura do código IL2CPP.

Como decodificar um payload de resposta/request
O script helper decrypt_payload.py faz o processo completo, seguindo exatamente a lógica do jogo:

import base64
import lz4.block
import msgpack
from Crypto.Cipher import AES

def decrypt_payload(payload_b64, key_hex, iv_hex):
    encrypted = base64.b64decode(payload_b64)
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad = decrypted[-1]
    decrypted = decrypted[:-pad]
    data = lz4.block.decompress(decrypted)
    return msgpack.unpackb(data, raw=False)
Uso
python decrypt_payload.py payload.txt 2f22172f31657bf41b835b6372a6221d <iv_em_hex>
payload.txt: Arquivo com o payload base64 puro capturado na request/response.

chave: "2f22172f31657bf41b835b6372a6221d" (extraída do WebAssembly .wasm)

IV: Deve ser extraído para cada requisição; é o vetor de inicialização da AES. Geralmente presente como prefixo, header ou conhecido em análise.

Onde cada etapa está documentada
Criptografia:

Dump e strings mostram "AES/CBC/PKCS7PADDING" (presente no metadata, confirmando PKCS7).

O código il2cpp referencia métodos como EncryptoBody, DecryptoBody e helpers em Aes256.

Compressão e serialização:

MessagePackSerializer com métodos ToLZ4BinaryCore e LZ4Operation (presentes em dump.cs).

Enumeração MessagePackCompression inclui Lz4Block e Lz4BlockArray.

Chave:

Extraída do .wasm via análise hex (ex: 2f22172f31657bf41b835b6372a6221d).

Estrutura das classes e requests:

Consultar dump.cs, buscar por: HttpClientBuilder, WebRequestClient, Aes256, MessagePackSerializer, etc.

Notas adicionais
Você pode auditar o processo inteiro usando os dumps.

O script de decode segue exatamente a ordem do código do jogo.

Não é necessário re-extrair metadata/dumps a cada análise (a não ser que o jogo atualize).

O IV muda a cada requisição; sempre extraia do request/response interceptada.

O script não cobre o handshake RSA do login (que serve só para exchange da chave AES, geralmente em requests autenticadas).

Referências rápidas
Il2CppDumper

MessagePack Python

LZ4 Python

PyCryptodome (AES)

Exemplo de uso prático

python decrypt_payload.py resposta_b64.txt 2f22172f31657bf41b835b6372a6221d d96ee94b1b3fdfb984b07974f7666b87
Se tiver dúvidas, é só buscar por strings de função/enum/constante nos dumps, ou consultar as etapas acima.

Se quiser um exemplo ainda mais prático (com entrada direta no código) ou um script que aceite payloads copiados do Charles ou Burp, só pedir!