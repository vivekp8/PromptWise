// src/components/PromptForm.tsx
import { useState } from "react";

export interface PromptData {
  user_id: string;
  prompt_id: string;
  content: string;
  model: string;
}

interface PromptFormProps {
  onSubmit: (data: PromptData) => void;
}

export default function PromptForm({ onSubmit }: PromptFormProps) {
  const [form, setForm] = useState<PromptData>({
    user_id: "user001",
    prompt_id: "p001",
    content: "",
    model: "text"
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit(form);
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "1rem" }}>
      <input name="user_id" value={form.user_id} onChange={handleChange} placeholder="User ID" />
      <input name="prompt_id" value={form.prompt_id} onChange={handleChange} placeholder="Prompt ID" />
      <textarea name="content" value={form.content} onChange={handleChange} placeholder="Enter your prompt..." />
      <select name="model" value={form.model} onChange={handleChange}>
        <option value="text">text</option>
        <option value="chat">chat</option>
      </select>
      <button type="submit">Submit Prompt</button>
    </form>
  );
}