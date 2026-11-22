import SkillList from "./SkillList";

export default function ResultPanel({ result, isLoading, error }) {
  if (isLoading) {
    return <p className="status-text">Reading your resume and comparing it with the job...</p>;
  }

  if (error) {
    return (
      <p className="form-error" role="alert">
        {error}
      </p>
    );
  }

  if (!result) {
    return (
      <p className="status-text">
        Nothing to show yet. Add your resume and a job description, then press Compare.
      </p>
    );
  }

  return (
    <div>
      <p className="score">{result.score}% estimated match</p>
      <p className="hint">
        This only measures how much your resume and the job text overlap. It cannot tell you
        whether you will be hired.
      </p>

      <SkillList
        title="Found in your resume"
        skills={result.matched_skills}
        variant="matched"
        emptyText="None of the skills in this job description were found in your resume."
      />
      <SkillList
        title="Missing from your resume"
        skills={result.missing_skills}
        variant="missing"
        emptyText="Your resume mentions every skill we found in this job description."
      />

      <h3>How the score was worked out</h3>
      <ul className="plain-list">
        {result.explanation.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>

      {result.suggestions.length > 0 && (
        <>
          <h3>What you could do</h3>
          <ul className="plain-list">
            {result.suggestions.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}