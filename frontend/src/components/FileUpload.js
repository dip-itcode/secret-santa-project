import React, { useRef, useState } from "react";

export default function FileUpload({ accept, label, onFile }) {
  const inputRef = useRef();
  const [fileName, setFileName] = useState(null);

  function handleChange(e) {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onFile(file);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setFileName(file.name);
      onFile(file);
    }
  }

  return (
    <div
      className="dropzone"
      onClick={() => inputRef.current.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        style={{ display: "none" }}
        onChange={handleChange}
      />
      {fileName ? (
        <span className="file-name">📄 {fileName}</span>
      ) : (
        <span className="dropzone-hint">📂 {label}</span>
      )}
    </div>
  );
}
