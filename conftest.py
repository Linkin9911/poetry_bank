import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Добавляем src/ в sys.path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
