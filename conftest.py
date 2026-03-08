import sys
from pathlib import Path

# Добавляем src/ в sys.path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
