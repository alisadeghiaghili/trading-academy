import { useEffect } from "react";
import { useAppStore } from "./store";

export function useLocale() {
  const { locale, setLocale } = useAppStore();

  useEffect(() => {
    document.documentElement.dir = locale === "fa" ? "rtl" : "ltr";
    document.documentElement.lang = locale;
  }, [locale]);

  return { locale, setLocale };
}

export function useTheme() {
  const { theme, setTheme } = useAppStore();

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("light", "dark");

    if (theme === "system") {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      root.classList.add(prefersDark ? "dark" : "light");
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  return { theme, setTheme };
}

export function useDocumentTitle(title?: string) {
  useEffect(() => {
    const original = document.title;
    document.title = title ? `${title} | Trading Academy` : "Trading Academy";
    return () => {
      document.title = original;
    };
  }, [title]);
}