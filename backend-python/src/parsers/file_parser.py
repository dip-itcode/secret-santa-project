"""
Parsers for reading employee and previous-assignment data from CSV / XLSX files.
"""
import csv
import io
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from src.models.employee import Employee, Assignment


class EmployeeParser:
    """Parses employee lists from CSV or XLSX files."""

    REQUIRED_COLS = {"Employee_Name", "Employee_EmailID"}

    def parse_file(self, filepath: str) -> List[Employee]:
        """Auto-detect format and parse the employee list."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
            return self._parse_excel(path)
        if path.suffix.lower() in (".csv", ".tsv"):
            return self._parse_csv(path)
        raise ValueError(f"Unsupported file format: {path.suffix}")

    def parse_csv_content(self, content: str) -> List[Employee]:
        """Parse employee list from a raw CSV string (e.g. from API upload)."""
        reader = csv.DictReader(io.StringIO(content))
        self._validate_columns(set(reader.fieldnames or []))
        return [
            Employee(name=row["Employee_Name"], email=row["Employee_EmailID"])
            for row in reader
            if row.get("Employee_Name") and row.get("Employee_EmailID")
        ]

    def _parse_csv(self, path: Path) -> List[Employee]:
        df = pd.read_csv(path)
        self._validate_columns(set(df.columns))
        return self._df_to_employees(df)

    def _parse_excel(self, path: Path) -> List[Employee]:
        df = pd.read_excel(path, engine="openpyxl")
        self._validate_columns(set(df.columns))
        return self._df_to_employees(df)

    @staticmethod
    def _df_to_employees(df: pd.DataFrame) -> List[Employee]:
        df = df.dropna(subset=["Employee_Name", "Employee_EmailID"])
        return [
            Employee(name=str(row["Employee_Name"]), email=str(row["Employee_EmailID"]))
            for _, row in df.iterrows()
        ]

    def _validate_columns(self, columns: set):
        missing = self.REQUIRED_COLS - columns
        if missing:
            raise ValueError(f"Missing required columns: {missing}")


class AssignmentParser:
    """Parses previous-year Secret Santa assignments from CSV / XLSX files."""

    REQUIRED_COLS = {
        "Employee_Name", "Employee_EmailID",
        "Secret_Child_Name", "Secret_Child_EmailID",
    }

    def parse_file(self, filepath: str) -> List[Assignment]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
            df = pd.read_excel(path, engine="openpyxl")
        else:
            df = pd.read_csv(path)
        self._validate_columns(set(df.columns))
        return self._df_to_assignments(df)

    def parse_csv_content(self, content: str) -> List[Assignment]:
        reader = csv.DictReader(io.StringIO(content))
        self._validate_columns(set(reader.fieldnames or []))
        return [self._row_to_assignment(row) for row in reader]

    @staticmethod
    def _df_to_assignments(df: pd.DataFrame) -> List[Assignment]:
        df = df.dropna(subset=["Employee_Name", "Employee_EmailID",
                                "Secret_Child_Name", "Secret_Child_EmailID"])
        return [
            Assignment(
                giver=Employee(name=str(r["Employee_Name"]), email=str(r["Employee_EmailID"])),
                receiver=Employee(name=str(r["Secret_Child_Name"]), email=str(r["Secret_Child_EmailID"])),
            )
            for _, r in df.iterrows()
        ]

    @staticmethod
    def _row_to_assignment(row: dict) -> Assignment:
        return Assignment(
            giver=Employee(name=row["Employee_Name"], email=row["Employee_EmailID"]),
            receiver=Employee(name=row["Secret_Child_Name"], email=row["Secret_Child_EmailID"]),
        )

    def _validate_columns(self, columns: set):
        missing = self.REQUIRED_COLS - columns
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
