// All communication with the FastAPI backend lives in this file.

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export async function analyzeResume(resumeFile, jobDescription) {
  // A file upload is sent as "form data", not as JSON.
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription);

  let response;
  try {
    response = await fetch(`${API_URL}/analyze`, { method: "POST", body: formData });
  } catch {
    throw new Error("Could not reach the server. Check that the backend is running.");
  }

  if (!response.ok) {
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
    throw new Error(message);
  }

  return response.json();
}