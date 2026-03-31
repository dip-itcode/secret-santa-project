"""
Validators for employee lists and assignment inputs.
"""
import re
from typing import List

from src.models.employee import Employee


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmployeeValidator:
    """Validates a list of employees before processing."""

    def validate(self, employees: List[Employee]) -> List[str]:
        """
        Returns a list of error strings. Empty list = valid.
        """
        errors: List[str] = []

        if not employees:
            errors.append("Employee list is empty.")
            return errors

        if len(employees) < 2:
            errors.append("At least 2 employees are required for Secret Santa.")

        emails_seen = set()
        for emp in employees:
            if not emp.name:
                errors.append(f"Employee has an empty name (email: {emp.email}).")
            if not emp.email:
                errors.append(f"Employee '{emp.name}' has an empty email.")
            elif not EMAIL_RE.match(emp.email):
                errors.append(f"Invalid email format: '{emp.email}' for employee '{emp.name}'.")
            elif emp.email in emails_seen:
                errors.append(f"Duplicate email detected: '{emp.email}'.")
            else:
                emails_seen.add(emp.email)

        return errors


class AssignmentInputValidator:
    """Validates that the provided inputs can produce a valid assignment."""

    def validate(self, employees: List[Employee], previous_assignments=None) -> List[str]:
        errors = EmployeeValidator().validate(employees)
        if errors:
            return errors

        if previous_assignments:
            prev_givers = {a.giver.email for a in previous_assignments}
            current_emails = {e.email for e in employees}
            unknown = prev_givers - current_emails
            if unknown:
                # Not a hard error — previous employees may have left the company
                pass  # handled gracefully in the service layer

        return []
