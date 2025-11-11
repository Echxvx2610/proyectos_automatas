import { Sun, Moon } from "lucide-react"
import "./Header.css"

function Header({ theme, onToggleTheme }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          {/* <Skull size={48} /> */}
          <img src="gigachad_circle.png" alt="gigachad" width={70} />
          <span>OpenChad</span>
        </div>
        <div className="header-actions">
          <button 
            onClick={onToggleTheme} 
            className="theme-toggle"
            title={theme === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
          >
            {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          <div className="status">
            <div className="status-dot"></div>
            <span>Conectado..</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
