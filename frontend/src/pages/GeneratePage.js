import React, { useState } from "react";
import toast from "react-hot-toast";
import FileUpload from "../components/FileUpload";
import AssignmentTable from "../components/AssignmentTable";
import ExportButtons from "../components/ExportButtons";
import { generateAssignments } from "../services/api";

export default function GeneratePage() {
  const [employeesFile, setEmployeesFile] = useState(null);
  const [previousFile, setPreviousFile] = useState(null);
  const [year, setYear] = useState(new Date().getFullYear());
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    if (!employeesFile) {
      toast.error("Please upload an employee file first.");
      return;
    }
    setLoading(true);
    try {
      const data = await generateAssignments(employeesFile, previousFile, year, "json");
      setAssignments(data.assignments || []);
      toast.success(`✅ ${data.total} assignments generated!`);
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.errors?.join(", ") || "Generation failed.";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1 className="page-title">🎁 Generate Assignments</h1>
        <p className="page-subtitle">Upload your employee list and run the Secret Santa draw.</p>

        <div className="form-grid">
          <div className="form-group">
            <label className="label">Employee List <span className="required">*</span></label>
            <FileUpload
              accept=".csv,.xlsx,.xls"
              label="Drop CSV or XLSX here"
              onFile={setEmployeesFile}
            />
          </div>

          <div className="form-group">
            <label className="label">Previous Year Assignments <span className="optional">(optional)</span></label>
            <FileUpload
              accept=".csv"
              label="Drop previous CSV here"
              onFile={setPreviousFile}
            />
          </div>

          <div className="form-group">
            <label className="label">Year</label>
            <input
              type="number"
              className="input"
              value={year}
              min={2000}
              max={2100}
              onChange={(e) => setYear(Number(e.target.value))}
            />
          </div>
        </div>

        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? "Generating…" : "🎲 Draw Names"}
        </button>
      </div>

      {assignments.length > 0 && (
        <div className="card">
          <div className="section-header">
            <h2 className="section-title">Results — {year}</h2>
            <ExportButtons assignments={assignments} year={year} />
          </div>
          <AssignmentTable assignments={assignments} />
        </div>
      )}
    </div>
  );
}
