import { useEffect, useState } from "react";
import {
  createApplication,
  deleteApplication,
  getApplicationStats,
  listAnalyses,
  listApplications,
  updateApplication,
} from "../api";
import { STATUSES } from "../statuses";
import ApplicationForm from "../components/ApplicationForm";
import ApplicationList from "../components/ApplicationList";
import StatsBar from "../components/StatsBar";

export default function TrackerPage() {
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(null);
  const [analyses, setAnalyses] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [sort, setSort] = useState("newest");
  const [refreshCount, setRefreshCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  // Load everything again whenever the filter, the sort order or refreshCount changes.
  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [appData, statsData, analysisData] = await Promise.all([
          listApplications(statusFilter, sort),
          getApplicationStats(),
          listAnalyses(),
        ]);
        if (cancelled) return;
        setApplications(appData);
        setStats(statsData);
        setAnalyses(analysisData);
        setError("");
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
  }, [statusFilter, sort, refreshCount]);

  function reload() {
    setRefreshCount((count) => count + 1);
  }

  async function handleAdd(application) {
    await createApplication(application); // errors are shown by the form
    reload();
  }

  async function handleStatusChange(application, newStatus) {
    try {
      await updateApplication(application.id, { status: newStatus });
      reload();
    } catch (problem) {
      setError(problem.message);
    }
  }

  async function handleDelete(application) {
    if (!window.confirm(`Delete the application for "${application.job_title}"?`)) {
      return;
    }
    try {
      await deleteApplication(application.id);
      reload();
    } catch (problem) {
      setError(problem.message);
    }
  }

  // Lets each application find its linked analysis quickly by id.
  const analysesById = Object.fromEntries(analyses.map((analysis) => [analysis.id, analysis]));

  return (
    <main className="single-column">
      <h2>Application tracker</h2>

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      {stats && <StatsBar stats={stats} />}

      <ApplicationForm analyses={analyses} onAdd={handleAdd} />

      <div className="list-controls">
        <div>
          <label htmlFor="filter-status">Show</label>
          <select
            id="filter-status"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="">All statuses</option>
            {STATUSES.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="sort-order">Sort by date</label>
          <select id="sort-order" value={sort} onChange={(event) => setSort(event.target.value)}>
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
          </select>
        </div>
      </div>

      {isLoading && <p className="status-text">Loading your applications...</p>}

      {!isLoading && !error && applications.length === 0 && (
        <p className="status-text">
          {statusFilter
            ? `No applications with the status ${statusFilter}.`
            : "No applications yet. Add the first one with the form above."}
        </p>
      )}

      <ApplicationList
        applications={applications}
        analysesById={analysesById}
        onStatusChange={handleStatusChange}
        onDelete={handleDelete}
      />
    </main>
  );
}