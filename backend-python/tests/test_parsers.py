"""
Tests for EmployeeParser and AssignmentParser.
"""
import os
import tempfile
import pytest

from src.parsers.file_parser import EmployeeParser, AssignmentParser


parser = EmployeeParser()
aparser = AssignmentParser()

VALID_CSV = "Employee_Name,Employee_EmailID\nAlice,alice@acme.com\nBob,bob@acme.com\n"
PREVIOUS_CSV = (
    "Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID\n"
    "Alice,alice@acme.com,Bob,bob@acme.com\n"
    "Bob,bob@acme.com,Alice,alice@acme.com\n"
)


class TestEmployeeParser:
    def test_parse_valid_csv_content(self):
        employees = parser.parse_csv_content(VALID_CSV)
        assert len(employees) == 2
        assert employees[0].name == "Alice"
        assert employees[1].email == "bob@acme.com"

    def test_parse_csv_file(self, tmp_path):
        f = tmp_path / "emp.csv"
        f.write_text(VALID_CSV)
        employees = parser.parse_file(str(f))
        assert len(employees) == 2

    def test_parse_missing_column_raises(self):
        bad = "Name,Email\nAlice,alice@acme.com\n"
        with pytest.raises(ValueError, match="Missing required columns"):
            parser.parse_csv_content(bad)

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            parser.parse_file("/nonexistent/path.csv")

    def test_parse_excel_file(self):
        """Integration test against the real uploaded file."""
        path = os.path.join(os.path.dirname(__file__), "../data/Employee-List.xlsx")
        if not os.path.exists(path):
            pytest.skip("Employee-List.xlsx not present")
        employees = parser.parse_file(path)
        assert len(employees) >= 2
        assert all(e.email for e in employees)


class TestAssignmentParser:
    def test_parse_valid_previous_csv(self):
        assignments = aparser.parse_csv_content(PREVIOUS_CSV)
        assert len(assignments) == 2
        assert assignments[0].giver.name == "Alice"
        assert assignments[0].receiver.name == "Bob"

    def test_missing_column_raises(self):
        bad = "Employee_Name,Employee_EmailID\nAlice,alice@acme.com\n"
        with pytest.raises(ValueError):
            aparser.parse_csv_content(bad)
