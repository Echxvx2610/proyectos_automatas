"use client"

import { useState } from "react"
import { Send } from "lucide-react"
import "./ChatInput.css"

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input)
      setInput("")
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-input-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe tu pregunta aquí..."
          disabled={disabled}
          rows={1}
          className="chat-input"
        />
        <button type="submit" disabled={disabled || !input.trim()} className="send-button">
          <Send size={20} />
        </button>
      </form>
      <div className="input-hint">Presiona Enter para enviar, Shift + Enter para nueva línea</div>
    </div>
  )
}

export default ChatInput
