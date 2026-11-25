import { useState } from "react";
import { Plus } from "lucide-react";
import { STATUSES } from "../statuses";

export default function ApplicationForm({ analyses, onAdd }) {
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [status, setStatus] = useState("Interested");
  const [notes, setNotes] = useState("");
  const [analysisId, setAnalysisId] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!jobTitle.trim()) {
      setError("Enter a job title.");
      return;
    }

    setIsSaving(true);
    setError("");
    try {
      await onAdd({
        job_title: jobTitle.trim(),
        company: company.trim(),
        status,
        notes: notes.trim(),
        analysis_id: analysisId === "" ? null : Number(analysisId),
      });
      setJobTitle("");
      setCompany("");
      setStatus("Interested");
      setNotes("");
      setAnalysisId("");
    } catch (problem) {
      setError(problem.message);
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <form className="sheet tracker-form" onSubmit={handleSubmit} noValidate>
      <h3>Add an application</h3>

      <div className="form-grid">
        <div className="field">
          <label htmlFor="app-title">Job title</label>
          <input
            id="app-title"
            type="text"
            value={jobTitle}
            onChange={(event) => setJobTitle(event.target.value)}
          />
        </div>

        <div className="field">
          <label htmlFor="app-company">Company (optional)</label>
          <input
            id="app-company"
            type="text"
            value={company}
            onChange={(event) => setCompany(event.target.value)}
          />
        </div>

        <div className="field">
          <label htmlFor="app-status">Status</label>
          <select id="app-status" value={status} onChange={(event) => setStatus(event.target.value)}>
            {STATUSES.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor="app-analysis">Saved analysis (optional)</label>
          <select
            id="app-analysis"
            value={analysisId}
            onChange={(event) => setAnalysisId(event.target.value)}
          >
            <option value="">None</option>
            {analyses.map((analysis) => (
              <option key={analysis.id} value={analysis.id}>
                {analysis.job_title}
                {analysis.company ? ` at ${analysis.company}` : ""} ({analysis.score}%)
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="field">
        <label htmlFor="app-notes">Notes (optional)</label>
        <textarea
          id="app-notes"
          rows={2}
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
        />
      </div>

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      <button type="submit" className="primary-button" disabled={isSaving}>
        <Plus size={18} aria-hidden="true" />
        {isSaving ? "Adding..." : "Add application"}
      </button>
    </form>
  );
}