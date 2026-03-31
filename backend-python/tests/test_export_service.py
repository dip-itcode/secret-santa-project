"""
Tests for ExportService (CSV and XML output).
"""
import csv
import io
import xml.etree.ElementTree as ET
import pytest

from src.services.export_service import ExportService
from src.models.employee import Employee, Assignment


service = ExportService()

ASSIGNMENTS = [
    Assignment(Employee("Alice", "alice@acme.com"), Employee("Bob", "bob@acme.com")),
    Assignment(Employee("Bob", "bob@acme.com"), Employee("Charlie", "charlie@acme.com")),
]


class TestCSVExport:
    def test_csv_has_header(self):
        out = service.to_csv(ASSIGNMENTS)
        reader = csv.DictReader(io.StringIO(out))
        assert set(reader.fieldnames) == {
            "Employee_Name", "Employee_EmailID",
            "Secret_Child_Name", "Secret_Child_EmailID",
        }

    def test_csv_row_count(self):
        out = service.to_csv(ASSIGNMENTS)
        rows = list(csv.DictReader(io.StringIO(out)))
        assert len(rows) == 2

    def test_csv_values_correct(self):
        out = service.to_csv(ASSIGNMENTS)
        rows = list(csv.DictReader(io.StringIO(out)))
        assert rows[0]["Employee_Name"] == "Alice"
        assert rows[0]["Secret_Child_Name"] == "Bob"


class TestXMLExport:
    def test_xml_is_parseable(self):
        out = service.to_xml(ASSIGNMENTS)
        root = ET.fromstring(out)
        assert root.tag == "SecretSantaAssignments"

    def test_xml_assignment_count(self):
        out = service.to_xml(ASSIGNMENTS)
        root = ET.fromstring(out)
        assert len(root.findall("Assignment")) == 2

    def test_xml_contains_correct_values(self):
        out = service.to_xml(ASSIGNMENTS)
        root = ET.fromstring(out)
        first = root.find("Assignment")
        assert first.find("Employee_Name").text == "Alice"
        assert first.find("Secret_Child_Name").text == "Bob"
