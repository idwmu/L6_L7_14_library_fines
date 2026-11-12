import pytest
from library_fines import late_fine, can_borrow, renewal_status

#Example test cases:
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0

def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

#Write the rest of the test cases so that the code is 90- 100% covered.


# ---------- late_fine ----------

def test_late_fine_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("staff", 10, False)

def test_late_fine_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

def test_late_fine_zero_days():
    assert late_fine("guest", 0, False) == 0

def test_late_fine_student_on_due_date():
    assert late_fine("student", 14, False) == 0

def test_late_fine_student_overdue():
    assert late_fine("student", 20, False) == 12

def test_late_fine_guest_overdue():
    assert late_fine("guest", 15, False) == 5

def test_late_fine_faculty_within_loan():
    assert late_fine("faculty", 30, False) == 0

def test_late_fine_faculty_overdue():
    assert late_fine("faculty", 40, False) == 10

def test_late_fine_exactly_at_cap():
    assert late_fine("student", 114, False) == 200

def test_late_fine_capped():
    assert late_fine("guest", 100, False) == 200

def test_late_fine_damaged_not_overdue():
    assert late_fine("student", 5, True) == 150

def test_late_fine_damaged_and_overdue():
    assert late_fine("student", 20, True) == 162

def test_late_fine_damaged_and_capped():
    assert late_fine("guest", 100, True) == 350


# ---------- can_borrow ----------

def test_can_borrow_pending_fine_too_high():
    assert can_borrow(0, 101, "student") is False

def test_can_borrow_pending_fine_at_limit():
    assert can_borrow(0, 100, "student") is True

def test_can_borrow_student_at_limit():
    assert can_borrow(3, 0, "student") is False

def test_can_borrow_guest_below_limit():
    assert can_borrow(2, 0, "guest") is True

def test_can_borrow_faculty_below_limit():
    assert can_borrow(9, 0, "faculty") is True

def test_can_borrow_faculty_at_limit():
    assert can_borrow(10, 0, "faculty") is False

def test_can_borrow_faculty_with_high_fine():
    assert can_borrow(0, 150, "faculty") is False


# ---------- renewal_status ----------

def test_renewal_denied_when_reserved():
    assert renewal_status(0, True, 5) == "denied"

def test_renewal_reservation_checked_before_limit():
    assert renewal_status(5, True, -3) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_limit_checked_before_overdue():
    assert renewal_status(3, False, -1) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"

def test_renewal_renewed():
    assert renewal_status(1, False, 3) == "renewed"

def test_renewal_renewed_on_last_day():
    assert renewal_status(0, False, 0) == "renewed"
