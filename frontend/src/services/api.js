/**
 * API service layer — all calls to the Flask backend go here.
 */
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

const api = axios.create({ baseURL: BASE });

/**
 * Generate Secret Santa assignments.
 * @param {File} employeesFile  - CSV or XLSX file
 * @param {File|null} previousFile - optional previous-year CSV
 * @param {number} year
 * @param {"json"|"csv"|"xml"} format
 */
export async function generateAssignments(employeesFile, previousFile, year, format = "json") {
  const form = new FormData();
  form.append("employees_file", employeesFile);
  form.append("year", String(year));
  form.append("format", format);
  if (previousFile) form.append("previous_file", previousFile);

  const res = await api.post("/assignments/generate", form, {
    responseType: format === "json" ? "json" : "blob",
  });
  return res.data;
}

/**
 * Fetch saved assignments for a given year.
 */
export async function fetchAssignmentsByYear(year) {
  const res = await api.get(`/assignments/${year}`);
  return res.data;
}

/**
 * List all years that have saved assignments.
 */
export async function fetchYears() {
  const res = await api.get("/assignments/years");
  return res.data.years;
}

/**
 * Download assignments in CSV or XML format for a saved year.
 */
export async function downloadAssignments(year, format = "csv") {
  const res = await api.get(`/assignments/${year}?format=${format}`, {
    responseType: "blob",
  });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `secret_santa_${year}.${format}`);
  document.body.appendChild(link);
  link.click();
  link.remove();
}
