import pytest
from datetime import datetime
from price_tracker import get_price_change

@pytest.fixture
def sample_file(tmp_path):
    data = [
        "Product A,2023-10-20,100.00",
        "Product A,2023-10-25,150.00",
        "Product A,2023-11-05,120.00",
        "Product B,2023-10-02,200.00",
        "Product B,2023-09-01,180.00",
    ]
    file = tmp_path / "sample.txt"
    file.write_text("\n".join(data))
    return str(file)

@pytest.mark.parametrize("product, today_str, expected", [
    ("Product A", "2023-11-15", 20.0),
    ("Product B", "2023-10-15", None),
    ("Product C", "2023-11-15", None),
    ("Product A", "2023-11-05", -30.0),
])
def test_price_changes(sample_file, product, today_str, expected):
    today = datetime.strptime(today_str, "%Y-%m-%d").date()
    result = get_price_change(sample_file, product, today)
    if expected is None:
        assert result is None
    else:
        assert result == pytest.approx(expected)