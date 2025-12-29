import React, { useEffect, useState } from 'react';
import axios from 'axios';

type AuditEntry = {
  timestamp: string;
  event: string;
  performed_by: string;
  details: Record<string, any>;
};

const AuditLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<AuditEntry[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/admin/audit-log")
      .then(res => setLogs(res.data));
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h2>📊 Audit Log Viewer</h2>
      {logs.map((log, idx) => (
        <div key={idx} style={{
          borderBottom: "1px solid #ccc",
          padding: "12px",
          marginBottom: "8px"
        }}>
          <strong>{log.event}</strong> by {log.performed_by}
          <br />
          <small>{new Date(log.timestamp).toLocaleString()}</small>
          <pre style={{
            backgroundColor: "#f4f4f4",
            padding: "8px",
            fontSize: "12px",
            overflowX: "auto"
          }}>
            {JSON.stringify(log.details, null, 2)}
          </pre>
        </div>
      ))}
    </div>
  );
};

export default AuditLogViewer;
