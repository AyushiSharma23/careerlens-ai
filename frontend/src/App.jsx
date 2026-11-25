import { NavLink, Route, Routes } from "react-router-dom";
import AnalyzePage from "./pages/AnalyzePage";
import SavedPage from "./pages/SavedPage";
import TrackerPage from "./pages/TrackerPage";

export default function App() {
  return (
    <>
      <header className="site-header">
        <div className="site-header-inner">
          <h1>CareerLens AI</h1>
          <p>
            Upload your resume, paste a job posting, and see which skills the job asks for that
            your resume does not mention yet.
          </p>
          <nav className="main-nav" aria-label="Main">
            <NavLink to="/" end>
              Analyze
            </NavLink>
            <NavLink to="/saved">Saved analyses</NavLink>
            <NavLink to="/tracker">Tracker</NavLink>
          </nav>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<AnalyzePage />} />
        <Route path="/saved" element={<SavedPage />} />
        <Route path="/tracker" element={<TrackerPage />} />
      </Routes>
    </>
  );
}