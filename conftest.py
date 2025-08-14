# conftest.py – añade la raíz del proyecto al PYTHONPATH para que los tests puedan importar el paquete backend.

import sys
from pathlib import Path

root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))