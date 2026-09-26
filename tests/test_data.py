from pathlib import Path

import pytest

from gadget_analysis.data import add_totals, load_responses

DATA_PATH = Path("data/respondents.csv")

PAPER_X = [
    45,
    42,
    44,
    63,
    63,
    51,
    59,
    60,
    50,
    65,
    65,
    43,
    72,
    67,
    66,
    61,
    55,
    45,
    31,
    58,
    42,
    59,
    60,
    47,
    54,
    61,
    62,
    66,
    57,
    51,
    55,
    74,
    63,
    63,
    46,
    59,
    47,
    67,
    57,
    45,
    57,
    65,
    45,
    58,
    51,
    52,
    70,
    45,
    47,
    53,
    57,
    58,
    65,
    43,
    45,
    62,
    48,
    66,
    63,
    66,
    71,
    66,
    60,
    63,
    61,
    50,
    55,
    46,
    67,
]

PAPER_Y = [
    40,
    39,
    44,
    58,
    58,
    48,
    47,
    49,
    47,
    52,
    58,
    44,
    61,
    58,
    56,
    55,
    42,
    42,
    27,
    49,
    28,
    56,
    60,
    51,
    47,
    56,
    46,
    51,
    63,
    44,
    56,
    70,
    54,
    49,
    48,
    61,
    41,
    61,
    48,
    42,
    52,
    55,
    42,
    56,
    54,
    45,
    64,
    45,
    55,
    50,
    45,
    54,
    55,
    42,
    42,
    41,
    44,
    55,
    48,
    70,
    42,
    59,
    56,
    52,
    67,
    47,
    48,
    33,
    53,
]


def _text(rows):
    header = (
        "respondent,"
        + ",".join(f"X{i}" for i in range(1, 16))
        + ","
        + ",".join(f"Y{i}" for i in range(1, 15))
    )
    lines = [f"{name}," + ",".join(str(v) for v in values) for name, values in rows]
    return header + "\n" + "\n".join(lines) + "\n"


def test_loads_real_dataset():
    df = load_responses(DATA_PATH)
    assert df.height == 69
    assert df.width == 30
    assert df.columns[0] == "respondent"
    assert df.columns[1] == "X1"
    assert df.columns[-1] == "Y14"


def test_totals_match_paper_series():
    df = add_totals(load_responses(DATA_PATH))
    assert df["x_total"].to_list() == PAPER_X
    assert df["y_total"].to_list() == PAPER_Y


def test_accepts_valid_file(tmp_path):
    path = tmp_path / "ok.csv"
    path.write_text(_text([("N1", [3] * 29), ("N2", [4] * 29)]))
    assert load_responses(path).height == 2


def test_rejects_out_of_range_value(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text(_text([("N1", [3] * 28 + [6])]))
    with pytest.raises(ValueError, match="1-5"):
        load_responses(path)


def test_rejects_missing_value(tmp_path):
    path = tmp_path / "null.csv"
    path.write_text(_text([("N1", [3] * 28 + [""])]))
    with pytest.raises(ValueError, match="missing"):
        load_responses(path)


def test_rejects_unknown_columns(tmp_path):
    path = tmp_path / "cols.csv"
    path.write_text(_text([("N1", [3] * 29)]).replace("X15", "X16"))
    with pytest.raises(ValueError, match="columns"):
        load_responses(path)


def test_rejects_duplicate_respondent(tmp_path):
    path = tmp_path / "dup.csv"
    path.write_text(_text([("N1", [3] * 29), ("N1", [4] * 29)]))
    with pytest.raises(ValueError, match="unique"):
        load_responses(path)
