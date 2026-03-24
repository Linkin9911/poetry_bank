from typing import Any
from typing import Dict
from typing import List
from typing import cast

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV‑файла."""
    try:
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
        result = df.to_dict("records")
        return cast(List[Dict[str, Any]], result)
    except Exception as e:
        print(f"Ошибка чтения CSV‑файла: {e}")
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel‑файла."""
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        result = df.to_dict("records")
        return cast(List[Dict[str, Any]], result)
    except Exception as e:
        print(f"Ошибка чтения Excel‑файла: {e}")
        return []
