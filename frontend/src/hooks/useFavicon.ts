import { useEffect } from "react";

export const useFavicon = (theme: "light" | "dark") => {
  useEffect(() => {
    const path = `/static/favicon-${theme}.ico`;
    const link = document.querySelector("link[rel='icon']");
    if (link) {
      link.setAttribute("href", path);
    }
  }, [theme]);
};