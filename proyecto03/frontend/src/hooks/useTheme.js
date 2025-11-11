import { useState, useEffect } from "react"

export function useTheme() {
  // Obtener tema guardado o usar 'dark' por defecto
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("openchad-theme")
    return savedTheme || "dark"
  })

  useEffect(() => {
    // Aplicar el tema al documento
    document.documentElement.setAttribute("data-theme", theme)
    
    // Guardar en localStorage
    localStorage.setItem("openchad-theme", theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "dark" ? "light" : "dark"))
  }

  return { theme, toggleTheme }
}
