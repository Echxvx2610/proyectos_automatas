import { User, Bot } from "lucide-react"
import "./ChatMessage.css"

function ChatMessage({ message }) {
  const isUser = message.sender === "user"

  return (
    <div className={`message ${isUser ? "message-user" : "message-ai"} ${message.isError ? "message-error" : ""}`}>
      <div className="message-avatar">{isUser ? <User size={20} /> : <Bot size={20} />}</div>
      <div className="message-content">
        {message.attachments && message.attachments.length > 0 && (
          <div className="message-attachments">
            {message.attachments.map((att) => (
              <div key={att.id} className="message-attachment">
                {att.type === "image" ? (
                  <img src={att.data || "/placeholder.svg"} alt={att.name} className="message-attachment-image" />
                ) : (
                  <div className="message-attachment-text">📄 {att.name}</div>
                )}
              </div>
            ))}
          </div>
        )}
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
