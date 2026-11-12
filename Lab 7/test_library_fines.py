from hypothesis import given, strategies as st
from library_fines import parse_member_id, total_fine, shelf_code


# Property: for any string (or None), the function must not crash.

@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {e!r} on input {s!r}"


# Explicit regression cases for the bugs fuzzing finds.

def test_parse_member_id_edge_cases():
    for bad in [None, "", "STU", "STU-", "STU-abc", "A-1-2"]:
        parse_member_id(bad)

def test_total_fine_edge_cases():
    for bad in [None, "", "10,,20", "abc", "10, ,5"]:
        total_fine(bad)

def test_shelf_code_edge_cases():
    for bad in [None, "", "Hello", "   "]:
        shelf_code(bad)


# Valid inputs must still give correct answers after hardening.

def test_valid_inputs_still_work():
    assert parse_member_id("STU-1023") == ("STU", 1023)
    assert total_fine("10,20,30") == (6 * 2) + (16 * 2)
    assert shelf_code("Introduction to Testing") == "IT"
