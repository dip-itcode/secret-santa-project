import React, { useState } from "react";

export default function AssignmentTable({ assignments }) {
  const [search, setSearch] = useState("");

  const filtered = assignments.filter(
    (a) =>
      a.Employee_Name.toLowerCase().includes(search.toLowerCase()) ||
      a.Secret_Child_Name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        className="input search-input"
        placeholder="🔍 Search by name…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="table-wrapper">
        <table className="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Giver Name</th>
              <th>Giver Email</th>
              <th>→</th>
              <th>Secret Child Name</th>
              <th>Secret Child Email</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((a, i) => (
              <tr key={i}>
                <td>{i + 1}</td>
                <td><strong>{a.Employee_Name}</strong></td>
                <td className="email">{a.Employee_EmailID}</td>
                <td className="arrow">🎁</td>
                <td><strong>{a.Secret_Child_Name}</strong></td>
                <td className="email">{a.Secret_Child_EmailID}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <p className="empty-state">No results match your search.</p>}
      </div>
    </div>
  );
}
