"""
MongoDB persistence layer for Secret Santa assignments.
"""
from datetime import datetime, timezone
from typing import List, Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from src.models.employee import Assignment, Employee


class MongoService:
    """Handles reading/writing assignments to MongoDB."""

    def __init__(self, uri: str, db_name: str = "secret_santa"):
        self._client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self._db = self._client[db_name]
        self._assignments = self._db["assignments"]

    def ping(self) -> bool:
        try:
            self._client.admin.command("ping")
            return True
        except ConnectionFailure:
            return False

    def save_assignments(self, assignments: List[Assignment], year: int) -> str:
        """Persist a batch of assignments for a given year. Returns inserted _id."""
        doc = {
            "year": year,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "assignments": [a.to_dict() for a in assignments],
        }
        result = self._assignments.insert_one(doc)
        return str(result.inserted_id)

    def get_assignments_by_year(self, year: int) -> Optional[List[Assignment]]:
        """Retrieve assignments for a given year, or None if not found."""
        doc = self._assignments.find_one({"year": year}, sort=[("created_at", -1)])
        if not doc:
            return None
        return [
            Assignment(
                giver=Employee(name=a["Employee_Name"], email=a["Employee_EmailID"]),
                receiver=Employee(name=a["Secret_Child_Name"], email=a["Secret_Child_EmailID"]),
            )
            for a in doc["assignments"]
        ]

    def list_years(self) -> List[int]:
        """Return all years that have saved assignments."""
        return sorted(self._assignments.distinct("year"))
