import os
import sys

from src.processing import filter_by_state
from src.processing import sort_by_date

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


if __name__ == "__main__":
    data = [{"state": "EXECUTED", "date": "2023-01-01"}, {"state": "CANCELED", "date": "2023-01-02"}]
    print(filter_by_state(data))
    print(sort_by_date(data))
