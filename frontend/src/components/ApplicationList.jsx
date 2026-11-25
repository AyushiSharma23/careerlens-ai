import { Trash2 } from "lucide-react";
import { STATUSES } from "../statuses";
import { formatDate } from "../utils";

export default function ApplicationList({ applications, analysesById, onStatusChange, onDelete }) {
  return (
    <ol className="saved-list">
      {applications.map((application) => {
        const linked = application.analysis_id ? analysesById[application.analysis_id] : null;

        return (
          <li key={application.id} className="sheet application-item">
            <div className="saved-item-head">
              <div>
                <h3>{application.job_title}</h3>
                <p className="hint">
                  {application.company ? `${application.company} · ` : ""}
                  Added on {formatDate(application.created_at)}
                </p>
              </div>

              <div className="status-picker">
                <label htmlFor={`status-${application.id}`}>Status</label>
                <select
                  id={`status-${application.id}`}
                  aria-label={`Status of ${application.job_title}`}
                  value={application.status}
                  onChange={(event) => onStatusChange(application, event.target.value)}
                >
                  {STATUSES.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {linked && (
              <p className="hint">
                Linked analysis: {linked.score}% estimated match, {linked.matched_skills.length}{" "}
                skills found, {linked.missing_skills.length} missing.
              </p>
            )}
            {application.notes && <p className="notes">{application.notes}</p>}

            <button type="button" className="text-button" onClick={() => onDelete(application)}>
              <Trash2 size={16} aria-hidden="true" />
              Delete
            </button>
          </li>
        );
      })}
    </ol>
  );
}