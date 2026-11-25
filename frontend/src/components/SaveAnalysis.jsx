import { useState } from "react";
import { Link } from "react-router-dom";
import { BookmarkPlus } from "lucide-react";
import { saveAnalysis } from "../api";

export default function SaveAnalysis({ submission }) {
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [error, setError] = useState("");

  async function handleSave(event) {
    event.preventDefault();

    if (!jobTitle.trim()) {
      setError("Enter a job title to save this analysis.");
      return;
    }

    setIsSaving(true);
    setError("");
    try {
      await saveAnalysis(
        submission.resumeFile,
        submission.jobDescription,
        jobTitle.trim(),
        company.trim(),
      );
      setIsSaved(true);
    } catch (problem) {
      setError(problem.message);
    } finally {
      setIsSaving(false);
    }
  }

  if (isSaved) {
    return (
      <p className="saved-note" role="status">
        Saved. <Link to="/saved">View your saved analyses</Link>.
      </p>
    );
  }

  return (
    <form className="save-form" onSubmit={handleSave} noValidate>
      <h3>Save this analysis</h3>

      <div className="field">
        <label htmlFor="job-title">Job title</label>
        <input
          id="job-title"
          type="text"
          value={jobTitle}
          onChange={(event) => setJobTitle(event.target.value)}
          placeholder="For example: Software Engineering Intern"
        />
      </div>

      <div className="field">
        <label htmlFor="company">Company (optional)</label>
        <input
          id="company"
          type="text"
          value={company}
          onChange={(event) => setCompany(event.target.value)}
        />
        <p className="hint">Your resume file is not stored. Only the job text and the results are.</p>
      </div>

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      <button type="submit" className="primary-button" disabled={isSaving}>
        <BookmarkPlus size={18} aria-hidden="true" />
        {isSaving ? "Saving..." : "Save analysis"}
      </button>
    </form>
  );
}