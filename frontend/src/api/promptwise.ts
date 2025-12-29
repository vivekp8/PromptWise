export interface PromptData {
  user_id: string;
  prompt_id: string;
  content: string;
  model: string;
}

export interface PromptResponse {
  session_id: string;
  response: string;
}

export async function submitPrompt(data: PromptData): Promise<PromptResponse> {
  const res = await fetch("http://localhost:8000/prompt/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function downloadPDF(session_id: string) {
  const res = await fetch(`http://localhost:8000/download/${session_id}`);
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `session_${session_id}.pdf`;
  a.click();
}
