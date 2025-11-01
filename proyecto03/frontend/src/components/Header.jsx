import { Sparkles } from "lucide-react"
import "./Header.css"

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <Sparkles size={48} />
          <span>OpenChad</span>
        </div>
        <div className="status">
          <div className="status-dot"></div>
          <span>Conectado..</span>
        </div>
      </div>
    </header>
  )
}

export default Header
