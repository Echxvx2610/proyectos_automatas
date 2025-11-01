import { User, Bot } from "lucide-react"
import "./ChatMessage.css"

function ChatMessage({ message }) {
  const isUser = message.sender === "user"

  return (
    <div className={`message ${isUser ? "message-user" : "message-ai"} ${message.isError ? "message-error" : ""}`}>
      <div className="message-avatar">{isUser ? <User size={20} /> : <Bot size={20} />}</div>
      <div className="message-content">
        <div className="message-text">{message.text}</div>
        <div className="message-time">
          {message.timestamp.toLocaleTimeString("es-ES", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
