import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";
import AssignmentTable from "../components/AssignmentTable";
import { fetchYears, fetchAssignmentsByYear, downloadAssignments } from "../services/api";

export default function HistoryPage() {
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchYears()
      .then(setYears)
      .catch(() => toast.error("Could not load history (is MongoDB configured?)"));
  }, []);

  async function handleYearSelect(y) {
    setSelectedYear(y);
    setLoading(true);
    try {
      const data = await fetchAssignmentsByYear(y);
      setAssignments(data.assignments);
    } catch {
      toast.error(`No data found for ${y}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1 className="page-title">📜 Assignment History</h1>
        <p className="page-subtitle">View and download past Secret Santa draws.</p>

        {years.length === 0 ? (
          <p className="empty-state">No saved assignments yet. Generate some first!</p>
        ) : (
          <div className="year-grid">
            {years.map((y) => (
              <button
                key={y}
                className={`year-btn ${selectedYear === y ? "active" : ""}`}
                onClick={() => handleYearSelect(y)}
              >
                {y}
              </button>
            ))}
          </div>
        )}
      </div>

      {selectedYear && (
        <div className="card">
          <div className="section-header">
            <h2 className="section-title">Assignments — {selectedYear}</h2>
            <div className="btn-group">
              <button className="btn btn-secondary" onClick={() => downloadAssignments(selectedYear, "csv")}>
                ⬇ CSV
              </button>
              <button className="btn btn-secondary" onClick={() => downloadAssignments(selectedYear, "xml")}>
                ⬇ XML
              </button>
            </div>
          </div>
          {loading ? <p>Loading…</p> : <AssignmentTable assignments={assignments} />}
        </div>
      )}
    </div>
  );
}
