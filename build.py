from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).parent
with ZipFile(root / 'dist/anki-ir.ankiaddon', 'w', ZIP_DEFLATED) as archive:
    for path in sorted((root / 'addon').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            archive.write(path, path.relative_to(root / 'addon'))
