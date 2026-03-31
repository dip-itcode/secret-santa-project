"""
Tests for SecretSantaService.
"""
import pytest
from src.services.secret_santa_service import SecretSantaService, AssignmentError
from src.models.employee import Employee, Assignment


service = SecretSantaService()


class TestBasicGeneration:
    def test_correct_number_of_assignments(self, employees):
        result = service.generate(employees)
        assert len(result) == len(employees)

    def test_no_self_assignment(self, employees):
        for _ in range(50):
            result = service.generate(employees)
            for a in result:
                assert a.giver.email != a.receiver.email

    def test_each_employee_is_giver_exactly_once(self, employees):
        result = service.generate(employees)
        givers = [a.giver.email for a in result]
        assert sorted(givers) == sorted(e.email for e in employees)

    def test_each_employee_is_receiver_exactly_once(self, employees):
        result = service.generate(employees)
        receivers = [a.receiver.email for a in result]
        assert sorted(receivers) == sorted(e.email for e in employees)


class TestPreviousYearConstraint:
    def test_no_repeat_from_last_year(self, employees, previous_assignments):
        prev_map = {a.giver.email: a.receiver.email for a in previous_assignments}
        for _ in range(50):
            result = service.generate(employees, previous_assignments)
            for a in result:
                assert prev_map.get(a.giver.email) != a.receiver.email, (
                    f"{a.giver.email} was assigned the same child as last year"
                )

    def test_ignores_previous_employees_no_longer_on_list(self, employees):
        ghost = Employee("Ghost", "ghost@acme.com")
        prev = [Assignment(ghost, employees[0])]
        result = service.generate(employees, prev)
        assert len(result) == len(employees)


class TestEdgeCases:
    def test_two_employees(self):
        a = Employee("A", "a@x.com")
        b = Employee("B", "b@x.com")
        result = service.generate([a, b])
        assert result[0].giver != result[0].receiver

    def test_raises_with_one_employee(self):
        with pytest.raises(AssignmentError):
            service.generate([Employee("Solo", "solo@x.com")])

    def test_raises_with_empty_list(self):
        with pytest.raises(AssignmentError):
            service.generate([])

    def test_deterministic_seed(self, employees):
        """Repeated calls should (almost always) produce different orders."""
        results = set()
        for _ in range(10):
            r = service.generate(employees)
            key = tuple(a.receiver.email for a in r)
            results.add(key)
        # With 5 employees there are many valid derangements — expect variety
        assert len(results) > 1
