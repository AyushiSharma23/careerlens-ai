import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Trash2 } from "lucide-react";
import { deleteAnalysis, listAnalyses } from "../api";
import SkillList from "../components/SkillList";
import { formatDate } from "../utils";


export default function SavedPage() {
  const [analyses, setAnalyses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await listAnalyses();
        if (!cancelled) setAnalyses(data);
      } catch (problem) {
        if (!cancelled) setError(problem.message);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleDelete(analysis) {
    if (!window.confirm(`Delete the saved analysis for "${analysis.job_title}"?`)) {
      return;
    }
    try {
      await deleteAnalysis(analysis.id);
      setAnalyses((current) => current.filter((item) => item.id !== analysis.id));
      setError("");
    } catch (problem) {
      setError(problem.message);
    }
  }

  return (
    <main className="single-column">
      <h2>Saved analyses</h2>

      {isLoading && <p className="status-text">Loading your saved analyses...</p>}

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      {!isLoading && !error && analyses.length === 0 && (
        <p className="status-text">
          You have not saved any analyses yet. Run a comparison on the{" "}
          <Link to="/">Analyze</Link> page and use "Save this analysis".
        </p>
      )}

      <ol className="saved-list">
        {analyses.map((analysis) => (
          <li key={analysis.id} className="sheet saved-item">
            <div className="saved-item-head">
              <div>
                <h3>{analysis.job_title}</h3>
                <p className="hint">
                  {analysis.company ? `${analysis.company} · ` : ""}
                  Saved on {formatDate(analysis.created_at)}
                </p>
              </div>
              <p className="saved-score">{analysis.score}% estimated match</p>
            </div>

            <details>
              <summary>Show skills and how the score was worked out</summary>
              <SkillList
                title="Found in your resume"
                skills={analysis.matched_skills}
                variant="matched"
                emptyText="None of the skills in this job description were found in your resume."
              />
              <SkillList
                title="Missing from your resume"
                skills={analysis.missing_skills}
                variant="missing"
                emptyText="Your resume mentions every skill we found in this job description."
              />
              <ul className="plain-list explanation">
                {analysis.explanation.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </details>

            <button type="button" className="text-button" onClick={() => handleDelete(analysis)}>
              <Trash2 size={16} aria-hidden="true" />
              Delete
            </button>
          </li>
        ))}
      </ol>
    </main>
  );
}