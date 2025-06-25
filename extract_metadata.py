import UnityPy
import sys
from pathlib import Path

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <input.data> <output_metadata>")
    sys.exit(1)

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])

env = UnityPy.load(str(input_path))
try:
    webfile = env.files[input_path.name]
except KeyError:
    raise RuntimeError(f"No WebFile found for {input_path}")
reader = webfile.files['Il2CppData/Metadata/global-metadata.dat']
output_path.write_bytes(reader.read(reader.Length))
print(f"Saved {output_path} ({output_path.stat().st_size} bytes)")