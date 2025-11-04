"use client"

import { useState, useRef, useEffect } from "react"
import ChatMessage from "./components/ChatMessage"
import ChatInput from "./components/ChatInput"
import Header from "./components/Header"
import Sidebar from "./components/Sidebar"
import "./App.css"

const API_URL = "http://localhost:5000/api"

function App() {
  const [chats, setChats] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    setIsMobile(window.innerWidth <= 768)

    const savedChats = localStorage.getItem("openchad-chats")
    if (savedChats) {
      const parsedChats = JSON.parse(savedChats)
      setChats(parsedChats)
      if (parsedChats.length > 0) {
        setCurrentChatId(parsedChats[0].id)
      }
    } else {
      // Create initial chat
      const initialChat = {
        id: Date.now(),
        title: "Nuevo Chat",
        messages: [],
        createdAt: new Date().toISOString(),
      }
      setChats([initialChat])
      setCurrentChatId(initialChat.id)
    }
  }, [])

  useEffect(() => {
    if (chats.length > 0) {
      localStorage.setItem("openchad-chats", JSON.stringify(chats))
    }
  }, [chats])

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 768)
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chats, currentChatId])

  const currentChat = chats.find((chat) => chat.id === currentChatId)
  const messages = currentChat?.messages || []

  const sendMessage = async (messageText, attachments = []) => {
    if (!messageText.trim() && attachments.length === 0) return

    let messageContent = messageText

    // Add attachment info to message
    if (attachments.length > 0) {
      const attachmentInfo = attachments
        .map((att) => {
          if (att.type === "image") {
            return `[Imagen: ${att.name}]`
          } else {
            return `[Archivo de texto: ${att.name}]\nContenido:\n${att.data}`
          }
        })
        .join("\n\n")

      messageContent = `${messageText}\n\n${attachmentInfo}`
    }

    const userMessage = {
      id: Date.now(),
      text: messageText,
      attachments: attachments,
      sender: "user",
      timestamp: new Date(),
    }

    setChats((prevChats) =>
      prevChats.map((chat) => {
        if (chat.id === currentChatId) {
          const updatedMessages = [...chat.messages, userMessage]
          // Update title if it's the first message
          const title =
            chat.messages.length === 0 ? messageText.slice(0, 30) + (messageText.length > 30 ? "..." : "") : chat.title
          return { ...chat, messages: updatedMessages, title }
        }
        return chat
      }),
    )

    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: messageContent }),
      })

      const data = await response.json()

      if (data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: "ai",
          timestamp: new Date(),
        }

        setChats((prevChats) =>
          prevChats.map((chat) => {
            if (chat.id === currentChatId) {
              return { ...chat, messages: [...chat.messages, aiMessage] }
            }
            return chat
          }),
        )
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

      setChats((prevChats) =>
        prevChats.map((chat) => {
          if (chat.id === currentChatId) {
            return { ...chat, messages: [...chat.messages, errorMessage] }
          }
          return chat
        }),
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: "Nuevo Chat",
      messages: [],
      createdAt: new Date().toISOString(),
    }
    setChats((prev) => [newChat, ...prev])
    setCurrentChatId(newChat.id)
  }

  const handleSelectChat = (chatId) => {
    setCurrentChatId(chatId)
  }

  const handleDeleteChat = (chatId) => {
    setChats((prev) => {
      const filtered = prev.filter((chat) => chat.id !== chatId)
      if (filtered.length === 0) {
        const newChat = {
          id: Date.now(),
          title: "Nuevo Chat",
          messages: [],
          createdAt: new Date().toISOString(),
        }
        setCurrentChatId(newChat.id)
        return [newChat]
      }
      if (currentChatId === chatId) {
        setCurrentChatId(filtered[0].id)
      }
      return filtered
    })
  }

  return (
    <div className="app">
      <Header />

      <div className="app-content">
        <Sidebar
          chats={chats}
          currentChatId={currentChatId}
          onNewChat={handleNewChat}
          onSelectChat={handleSelectChat}
          onDeleteChat={handleDeleteChat}
          isMobile={isMobile}
        />

        <div className="main-content">
          <div className="chat-container">
            {messages.length === 0 ? (
              <div className="welcome-screen">
                <div className="welcome-icon">🪄</div>
                <h1>Platica con OpenChad</h1>
                <p>Haz cualquier pregunta y obtén respuestas inteligentes</p>
                <div className="suggestions">
                  <button onClick={() => sendMessage("Quien eres? manifiestate!")}>¿Quien eres?</button>
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
      </div>
    </div>
  )
}

export default App
