import React from "react";
import toast from "react-hot-toast";
import { generateAssignments } from "../services/api";

export default function ExportButtons({ employeesFile, previousFile, year }) {
  async function handleDownload(format) {
    if (!employeesFile) return;
    try {
      const blob = await generateAssignments(employeesFile, previousFile, year, format);
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `secret_santa_${year}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      toast.error(`Failed to download ${format.toUpperCase()}`);
    }
  }

  return (
    <div className="btn-group">
      <button className="btn btn-secondary" onClick={() => handleDownload("csv")}>⬇ CSV</button>
      <button className="btn btn-secondary" onClick={() => handleDownload("xml")}>⬇ XML</button>
    </div>
  );
}
