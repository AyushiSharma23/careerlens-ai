import { useState } from "react";
import { FileUp } from "lucide-react";

export default function UploadForm({ onAnalyze, isLoading }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [formError, setFormError] = useState("");

  function handleSubmit(event) {
    event.preventDefault(); // stop the browser from reloading the page

    if (!resumeFile) {
      setFormError("Choose a PDF resume first.");
      return;
    }
    if (!jobDescription.trim()) {
      setFormError("Paste the job description first.");
      return;
    }

    setFormError("");
    onAnalyze(resumeFile, jobDescription);
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="field">
        <label htmlFor="resume">Resume (PDF)</label>
        <input
          id="resume"
          type="file"
          accept="application/pdf,.pdf"
          onChange={(event) => setResumeFile(event.target.files[0] ?? null)}
        />
        <p className="hint">
          {resumeFile ? `Selected: ${resumeFile.name}` : "Maximum size 5 MB. Scanned images are not supported."}
        </p>
      </div>

      <div className="field">
        <label htmlFor="job-description">Job description</label>
        <textarea
          id="job-description"
          rows={10}
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
          placeholder="Paste the full job description here"
        />
      </div>

      {formError && (
        <p className="form-error" role="alert">
          {formError}
        </p>
      )}

      <button type="submit" className="primary-button" disabled={isLoading}>
        <FileUp size={18} aria-hidden="true" />
                {isLoading ? "Comparing..." : "Compare"}
      </button>
    </form>
  );
}