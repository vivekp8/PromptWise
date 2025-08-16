import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';

type Props = {
  setUserRole: (role: string) => void;
};

const LoginForm: React.FC<Props> = ({ setUserRole }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8000/login", { username, password });
      localStorage.setItem("access_token", res.data.access_token);
      setUserRole(res.data.role);
      toast.success("✅ Login successful");
    } catch {
      toast.error("❌ Login failed");
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h3>🔐 Login to PromptWise</h3>
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
        style={{ marginBottom: "8px", padding: "6px", width: "200px" }}
      /><br />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        placeholder="Password"
        style={{ marginBottom: "16px", padding: "6px", width: "200px" }}
      /><br />
      <button onClick={handle