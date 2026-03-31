"""
Secret Santa assignment engine.

Rules:
  1. An employee cannot be their own secret child.
  2. An employee cannot be assigned the same secret child as last year.
  3. Each employee has exactly one secret child.
  4. Each secret child is assigned to exactly one employee.
"""
import random
from typing import List, Optional, Set, Dict

from src.models.employee import Employee, Assignment


class AssignmentError(Exception):
    """Raised when no valid assignment can be generated."""


class SecretSantaService:
    """Generates a valid Secret Santa assignment list."""

    MAX_RETRIES = 1000

    def generate(
        self,
        employees: List[Employee],
        previous_assignments: Optional[List[Assignment]] = None,
    ) -> List[Assignment]:
        """
        Generate assignments using a shuffle-and-verify approach with retries.

        Args:
            employees: Current employee list.
            previous_assignments: Last year's assignments (may be None).

        Returns:
            List of Assignment objects.

        Raises:
            AssignmentError: If no valid derangement can be found after MAX_RETRIES.
        """
        if len(employees) < 2:
            raise AssignmentError("Need at least 2 employees for Secret Santa.")

        previous_map: Dict[str, str] = {}  # giver_email → receiver_email
        if previous_assignments:
            for a in previous_assignments:
                previous_map[a.giver.email] = a.receiver.email

        for attempt in range(self.MAX_RETRIES):
            result = self._try_assign(employees, previous_map)
            if result is not None:
                return result

        raise AssignmentError(
            f"Could not generate a valid Secret Santa assignment after "
            f"{self.MAX_RETRIES} attempts. Check for constraint conflicts."
        )

    def _try_assign(
        self,
        employees: List[Employee],
        previous_map: Dict[str, str],
    ) -> Optional[List[Assignment]]:
        """Single attempt at building a valid derangement."""
        givers = employees[:]
        receivers = employees[:]
        random.shuffle(receivers)

        assignments: List[Assignment] = []
        for giver, receiver in zip(givers, receivers):
            if not self._is_valid_pair(giver, receiver, previous_map):
                return None
            assignments.append(Assignment(giver=giver, receiver=receiver))

        return assignments

    @staticmethod
    def _is_valid_pair(
        giver: Employee,
        receiver: Employee,
        previous_map: Dict[str, str],
    ) -> bool:
        """Return True only if this giver→receiver pairing is allowed."""
        # Rule 1: cannot self-assign
        if giver.email == receiver.email:
            return False
        # Rule 2: cannot repeat previous year's assignment
        if previous_map.get(giver.email) == receiver.email:
            return False
        return True
