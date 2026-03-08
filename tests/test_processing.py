import os
import sys
from typing import Any
from typing import Dict
from typing import List

import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"state": "EXECUTED", "date": "2023-01-01"},
        {"state": "PENDING", "date": "2023-01-02"},
        {"state": "CANCELED", "date": "2023-01-03"},
    ]


@pytest.mark.parametrize("state_filter,expected_count", [("EXECUTED", 1), ("PENDING", 1), ("UNKNOWN", 0)])
def test_filter_by_state(sample_transactions: List[Dict[str, Any]], state_filter: str, expected_count: int) -> None:
    filtered = filter_by_state(sample_transactions, state_filter)
    assert len(filtered) == expected_count


def test_sort_by_date_desc(sample_transactions: List[Dict[str, Any]]) -> None:
    sorted_transactions = sort_by_date(sample_transactions, reverse=True)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == sorted(dates, reverse=True)
