"use client"

import { useState, useRef, useEffect } from "react"
import ChatMessage from "./components/ChatMessage"
import ChatInput from "./components/ChatInput"
import Header from "./components/Header"
import "./App.css"
import { Wand } from "lucide-react"
const API_URL = "http://localhost:5000/api"

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return

    // Agregar mensaje del usuario
    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: messageText }),
      })

      const data = await response.json()

      if (data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: "ai",
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, aiMessage])
      } else {
        throw new Error(data.error || "Error al obtener respuesta")
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Error: ${error.message}. Verifica que el backend esté corriendo y la API key esté configurada.`,
        sender: "ai",
        timestamp: new Date(),
        isError: true,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <Header />

      <div className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-icon">🪄</div>
            {/* <div className="welcom-icon">
            <Wand size={64}/>
            </div> */}
            <h1>Chat con OpenChad</h1>
            <p>Haz cualquier pregunta y obtén respuestas inteligentes</p>
            <div className="suggestions">
              <button onClick={() => sendMessage("¿Qué es la inteligencia artificial?")}>¿Qué es la IA?</button>
              <button onClick={() => sendMessage("Explícame cómo funciona el aprendizaje automático")}>
                Aprendizaje automático
              </button>
              <button onClick={() => sendMessage("Dame consejos para programar mejor")}>
                Consejos de programación
              </button>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="loading-indicator">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  )
}

export default App
