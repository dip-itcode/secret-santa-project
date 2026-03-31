"""
Export service: converts assignments to CSV string or XML string.
"""
import csv
import io
import xml.etree.ElementTree as ET
from typing import List

from src.models.employee import Assignment


class ExportService:
    """Serialises assignment results to multiple formats."""

    CSV_FIELDS = [
        "Employee_Name",
        "Employee_EmailID",
        "Secret_Child_Name",
        "Secret_Child_EmailID",
    ]

    def to_csv(self, assignments: List[Assignment]) -> str:
        """Return a CSV string of assignments."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.CSV_FIELDS)
        writer.writeheader()
        for a in assignments:
            writer.writerow(a.to_dict())
        return output.getvalue()

    def to_xml(self, assignments: List[Assignment]) -> str:
        """Return a pretty-printed XML string of assignments."""
        root = ET.Element("SecretSantaAssignments")
        for a in assignments:
            entry = ET.SubElement(root, "Assignment")
            for key, val in a.to_xml_dict().items():
                child = ET.SubElement(entry, key)
                child.text = val
        self._indent(root)
        return ET.tostring(root, encoding="unicode", xml_declaration=False)

    @staticmethod
    def _indent(elem: ET.Element, level: int = 0):
        """In-place pretty-print indentation for ElementTree."""
        indent = "\n" + "  " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                ExportService._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent
