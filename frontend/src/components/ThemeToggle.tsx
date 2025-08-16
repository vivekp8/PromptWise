import { useState } from "react";

const ThemeToggle = ({ setTheme }: { setTheme: (t: "light" | "dark") => void }) => {
  const [mode, setMode] = useState<"light" | "dark">("light");

  const toggleTheme = () => {
    const newTheme = mode === "light" ? "dark" : "light";
    setMode(newTheme);
    setTheme(newTheme);
  };

  return (
    <button onClick={toggleTheme} style={{ marginBottom: "20px" }}>
      Switch to {mode === "light" ? "🌙 Dark" : "☀️ Light"} Mode
    </button>
  );
};

export default ThemeToggle;