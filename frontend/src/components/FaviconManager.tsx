import { useEffect } from "react";

const FaviconManager = ({ theme }: { theme: "light" | "dark" }) => {
  useEffect(() => {
    const href = `/static/favicon-${theme}.ico`;
    let link = document.querySelector("link[rel='icon']");

    if (!link) {
      link = document.createElement("link");
      link.rel = "icon";
      document.head.appendChild(link);
    }

    link.setAttribute("href", href);
  }, [theme]);

  return null;
};

export default FaviconManager;