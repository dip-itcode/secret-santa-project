import React from "react";
import toast from "react-hot-toast";

function exportToCsv(assignments, year) {
  const headers = ["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"];
  const csvContent = [
    headers.join(","),
    ...assignments.map(a => 
      `${a.Employee_Name},${a.Employee_EmailID},${a.Secret_Child_Name},${a.Secret_Child_EmailID}`
    )
  ].join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `secret_santa_${year}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function exportToXml(assignments, year) {
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<SecretSantaAssignments>\n`;
  for (const a of assignments) {
    xml += `  <Assignment>\n`;
    xml += `    <Employee_Name>${escapeXml(a.Employee_Name)}</Employee_Name>\n`;
    xml += `    <Employee_EmailID>${escapeXml(a.Employee_EmailID)}</Employee_EmailID>\n`;
    xml += `    <Secret_Child_Name>${escapeXml(a.Secret_Child_Name)}</Secret_Child_Name>\n`;
    xml += `    <Secret_Child_EmailID>${escapeXml(a.Secret_Child_EmailID)}</Secret_Child_EmailID>\n`;
    xml += `  </Assignment>\n`;
  }
  xml += `</SecretSantaAssignments>`;

  const blob = new Blob([xml], { type: "application/xml;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `secret_santa_${year}.xml`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function escapeXml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

export default function ExportButtons({ assignments, year }) {
  function handleDownload(format) {
    if (!assignments || assignments.length === 0) {
      toast.error("No assignments to export");
      return;
    }
    try {
      if (format === "csv") {
        exportToCsv(assignments, year);
      } else {
        exportToXml(assignments, year);
      }
      toast.success(`Downloaded ${format.toUpperCase()}`);
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
