// src/components/ResponseViewer.tsx
interface Props {
  session_id: string;
  response: string;
  onDownload: () => void;
}

export default function ResponseViewer({ session_id, response, onDownload }: Props) {
  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>Session ID: {session_id}</h3>
      <pre>{response}</pre>
      <button onClick={onDownload}>Download PDF</button>
    </div>
  );
}