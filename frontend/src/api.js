// All communication with the FastAPI backend lives in this file.

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function readErrorMessage(response) {
  let message = "Something went wrong. Please try again.";
  try {
    const data = await response.json();
    // Our own errors send a text message. Validation errors send a list, so we keep the default.
    if (typeof data.detail === "string") {
      message = data.detail;
    }
  } catch {
    // The response had no readable JSON, so the default message is used.
  }
  return message;
}

// Sends a request and turns every kind of failure into an Error with a readable message.
async function send(path, options) {
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, options);
  } catch {
    throw new Error("Could not reach the server. Check that the backend is running.");
  }

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response;
}

// A file upload is sent as "form data", not as JSON.
function buildForm(resumeFile, jobDescription) {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription);
  return formData;
}

export async function analyzeResume(resumeFile, jobDescription) {
  const response = await send("/analyze", {
    method: "POST",
    body: buildForm(resumeFile, jobDescription),
  });
  return response.json();
}

export async function saveAnalysis(resumeFile, jobDescription, jobTitle, company) {
  const formData = buildForm(resumeFile, jobDescription);
  formData.append("job_title", jobTitle);
  formData.append("company", company);

  const response = await send("/analyses", { method: "POST", body: formData });
  return response.json();
}

export async function listAnalyses() {
  const response = await send("/analyses");
  return response.json();
}

export async function deleteAnalysis(analysisId) {
  await send(`/analyses/${analysisId}`, { method: "DELETE" });
}