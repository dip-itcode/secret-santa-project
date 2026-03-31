"""
Shared pytest fixtures.
"""
import sys
import os
import pytest

# Make sure src/ is importable from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.employee import Employee, Assignment
from src.config.app_factory import create_app


@pytest.fixture
def employees():
    return [
        Employee("Alice", "alice@acme.com"),
        Employee("Bob", "bob@acme.com"),
        Employee("Charlie", "charlie@acme.com"),
        Employee("Diana", "diana@acme.com"),
        Employee("Eve", "eve@acme.com"),
    ]


@pytest.fixture
def previous_assignments(employees):
    # Alice→Bob, Bob→Charlie, Charlie→Diana, Diana→Eve, Eve→Alice
    return [
        Assignment(employees[0], employees[1]),
        Assignment(employees[1], employees[2]),
        Assignment(employees[2], employees[3]),
        Assignment(employees[3], employees[4]),
        Assignment(employees[4], employees[0]),
    ]


@pytest.fixture
def flask_client():
    app = create_app({"TESTING": True, "MONGO_URI": ""})
    with app.test_client() as client:
        yield client
