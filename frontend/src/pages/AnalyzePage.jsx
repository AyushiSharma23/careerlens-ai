import { useState } from "react";
import { analyzeResume } from "../api";
import UploadForm from "../components/UploadForm";
import ResultPanel from "../components/ResultPanel";
import SaveAnalysis from "../components/SaveAnalysis";

export default function AnalyzePage() {
  const [result, setResult] = useState(null);
  const [submission, setSubmission] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(resumeFile, jobDescription) {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeResume(resumeFile, jobDescription);
      setResult(data);
      // Keep what was submitted, so the same resume and job text can be saved afterwards.
      setSubmission({ id: Date.now(), resumeFile, jobDescription });
    } catch (problem) {
      setError(problem.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="layout">
      <section aria-labelledby="form-heading">
        <h2 id="form-heading">Your resume and the job</h2>
        <UploadForm onAnalyze={handleAnalyze} isLoading={isLoading} />
      </section>

      <section className="sheet" aria-labelledby="result-heading" aria-live="polite">
        <h2 id="result-heading">Comparison</h2>
        <ResultPanel result={result} isLoading={isLoading} error={error} />
        {result && submission && <SaveAnalysis key={submission.id} submission={submission} />}
      </section>
    </main>
  );
}