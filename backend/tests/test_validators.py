"""
Tests for input validators.
"""
import pytest
from src.validators.input_validator import EmployeeValidator
from src.models.employee import Employee


validator = EmployeeValidator()


class TestEmployeeValidator:
    def test_valid_list_returns_no_errors(self, employees):
        errors = validator.validate(employees)
        assert errors == []

    def test_empty_list_returns_error(self):
        errors = validator.validate([])
        assert any("empty" in e.lower() for e in errors)

    def test_single_employee_returns_error(self):
        errors = validator.validate([Employee("Alice", "alice@x.com")])
        assert len(errors) > 0

    def test_invalid_email_returns_error(self):
        employees = [
            Employee("Alice", "not-an-email"),
            Employee("Bob", "bob@acme.com"),
        ]
        errors = validator.validate(employees)
        assert any("invalid email" in e.lower() for e in errors)

    def test_duplicate_email_returns_error(self):
        employees = [
            Employee("Alice", "same@acme.com"),
            Employee("Bob", "same@acme.com"),
        ]
        errors = validator.validate(employees)
        assert any("duplicate" in e.lower() for e in errors)
