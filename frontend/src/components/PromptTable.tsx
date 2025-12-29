import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';

type Prompt = {
  id: string;
  title: string;
};

const PromptTable: React.FC = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/prompts")
      .then(res => setPrompts(res.data))
      .catch(() => toast.error("❌ Failed to load prompts"));
  }, []);

  const handleAction = async (id: string, type: "approve" | "reject") => {
    const endpoint = type === "approve"
      ? `/admin/prompts/${id}/approve`
      : `/admin/prompts/${id}/reject`;

    const payload = type === "approve"
      ? { comment: "Approved from PromptTable" }
      : { reason: "Needs revision" };

    toast.promise(
      axios.post(`http://localhost:8000${endpoint}`, payload),
      {
        loading: `${type === "approve" ? "Approving" : "Rejecting"}...`,
        success: `✅ Prompt ${type}d successfully`,
        error: `❌ Failed to ${type} prompt`
      }
    );
  };

  return (
    <div style={{ padding: "24px" }}>
      <h2>📋 Prompt List</h2>
      {prompts.map(prompt => (
        <div key={prompt.id} style={{
          marginBottom: "16px",
          padding: "12px",
          border: "1px solid #ccc",
          borderRadius: "8px"
        }}>
          <strong>{prompt.title}</strong>
          <br />
          <button onClick={() => handleAction(prompt.id, "approve")} style={{ marginRight: "8px" }}>
            ✅ Approve
          </button>
          <button onClick={() => handleAction(prompt.id, "reject")}>
            ❌ Reject
          </button>
        </div>
      ))}
    </div>
  );
};

export default PromptTable;
