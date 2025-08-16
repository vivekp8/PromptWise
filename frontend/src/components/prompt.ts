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