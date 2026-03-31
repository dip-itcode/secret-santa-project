"""
Employee model representing a participant in the Secret Santa game.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Employee:
    """Represents an employee participating in the Secret Santa game."""
    name: str
    email: str

    def __post_init__(self):
        self.name = self.name.strip()
        self.email = self.email.strip().lower()

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)

    def __repr__(self):
        return f"Employee(name={self.name!r}, email={self.email!r})"

    def to_dict(self) -> dict:
        return {"Employee_Name": self.name, "Employee_EmailID": self.email}


@dataclass
class Assignment:
    """Represents a Secret Santa assignment: one giver → one secret child."""
    giver: Employee
    receiver: Employee

    def to_dict(self) -> dict:
        return {
            "Employee_Name": self.giver.name,
            "Employee_EmailID": self.giver.email,
            "Secret_Child_Name": self.receiver.name,
            "Secret_Child_EmailID": self.receiver.email,
        }

    def to_xml_dict(self) -> dict:
        """Returns a flat dict suitable for XML serialisation."""
        return self.to_dict()
