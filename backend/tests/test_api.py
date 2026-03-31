"""
Integration tests for the Flask REST API.
"""
import io
import pytest


VALID_CSV = (
    "Employee_Name,Employee_EmailID\n"
    "Alice,alice@acme.com\n"
    "Bob,bob@acme.com\n"
    "Charlie,charlie@acme.com\n"
    "Diana,diana@acme.com\n"
    "Eve,eve@acme.com\n"
)


def _upload(client, csv_content=VALID_CSV, fmt="json", prev_csv=None):
    data = {
        "employees_file": (io.BytesIO(csv_content.encode()), "employees.csv"),
        "format": fmt,
        "year": "2025",
    }
    if prev_csv:
        data["previous_file"] = (io.BytesIO(prev_csv.encode()), "previous.csv")
    return client.post(
        "/api/assignments/generate",
        data=data,
        content_type="multipart/form-data",
    )


class TestHealthEndpoint:
    def test_health_returns_ok(self, flask_client):
        r = flask_client.get("/api/health")
        assert r.status_code == 200
        assert r.json["status"] == "ok"


class TestGenerateEndpoint:
    def test_returns_200_with_valid_csv(self, flask_client):
        r = _upload(flask_client)
        assert r.status_code == 200

    def test_returns_correct_assignment_count(self, flask_client):
        r = _upload(flask_client)
        assert r.json["total"] == 5

    def test_no_self_assignment_in_response(self, flask_client):
        r = _upload(flask_client)
        for a in r.json["assignments"]:
            assert a["Employee_EmailID"] != a["Secret_Child_EmailID"]

    def test_missing_file_returns_400(self, flask_client):
        r = flask_client.post("/api/assignments/generate",
                              data={}, content_type="multipart/form-data")
        assert r.status_code == 400

    def test_bad_csv_columns_returns_422(self, flask_client):
        bad = "Name,Email\nAlice,alice@acme.com\n"
        r = _upload(flask_client, csv_content=bad)
        assert r.status_code == 422

    def test_csv_format_response(self, flask_client):
        r = _upload(flask_client, fmt="csv")
        assert r.status_code == 200
        assert "text/csv" in r.content_type

    def test_xml_format_response(self, flask_client):
        r = _upload(flask_client, fmt="xml")
        assert r.status_code == 200
        assert "xml" in r.content_type

    def test_previous_assignments_respected(self, flask_client):
        prev = (
            "Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID\n"
            "Alice,alice@acme.com,Bob,bob@acme.com\n"
            "Bob,bob@acme.com,Charlie,charlie@acme.com\n"
            "Charlie,charlie@acme.com,Diana,diana@acme.com\n"
            "Diana,diana@acme.com,Eve,eve@acme.com\n"
            "Eve,eve@acme.com,Alice,alice@acme.com\n"
        )
        prev_map = {
            "alice@acme.com": "bob@acme.com",
            "bob@acme.com": "charlie@acme.com",
            "charlie@acme.com": "diana@acme.com",
            "diana@acme.com": "eve@acme.com",
            "eve@acme.com": "alice@acme.com",
        }
        r = _upload(flask_client, prev_csv=prev)
        assert r.status_code == 200
        for a in r.json["assignments"]:
            assert prev_map.get(a["Employee_EmailID"]) != a["Secret_Child_EmailID"]
