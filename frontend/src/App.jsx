import { useState } from "react";
import { analyzeResume } from "./api";
import UploadForm from "./components/UploadForm";
import ResultPanel from "./components/ResultPanel";

export default function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(resumeFile, jobDescription) {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeResume(resumeFile, jobDescription);
      setResult(data);
    } catch (problem) {
      setError(problem.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <header className="site-header">
        <div className="site-header-inner">
          <h1>CareerLens AI</h1>
          <p>
            Upload your resume, paste a job posting, and see which skills the job asks for that
            your resume does not mention yet.
          </p>
        </div>
      </header>

      <main className="layout">
        <section aria-labelledby="form-heading">
          <h2 id="form-heading">Your resume and the job</h2>
          <UploadForm onAnalyze={handleAnalyze} isLoading={isLoading} />
        </section>

        <section className="sheet" aria-labelledby="result-heading" aria-live="polite">
          <h2 id="result-heading">Comparison</h2>
          <ResultPanel result={result} isLoading={isLoading} error={error} />
        </section>
      </main>
    </>
  );
}