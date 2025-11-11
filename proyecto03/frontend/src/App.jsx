"use client"

import { useState, useRef, useEffect } from "react"
import ChatMessage from "./components/ChatMessage"
import ChatInput from "./components/ChatInput"
import Header from "./components/Header"
import Sidebar from "./components/Sidebar"
import { useTheme } from "./hooks/useTheme"
import "./App.css"

const API_URL = "http://localhost:5000/api"

function App() {
  const [chats, setChats] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const messagesEndRef = useRef(null)
  const abortControllerRef = useRef(null)
  const { theme, toggleTheme } = useTheme()

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
      // Crea el chat inicial si no hay chats guardados
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

  const sendMessage = async (messageText, attachments = [], pdfFile = null) => {
    if (!messageText.trim() && attachments.length === 0 && !pdfFile) return

    const userMessage = {
      id: Date.now(),
      text: messageText,
      attachments: attachments,
      pdfFile: pdfFile ? { name: pdfFile.name } : null,
      sender: "user",
      timestamp: new Date(),
    }

    setChats((prevChats) =>
      prevChats.map((chat) => {
        if (chat.id === currentChatId) {
          const updatedMessages = [...chat.messages, userMessage]
          // actualizar el título si es el primer mensaje
          const title =
            chat.messages.length === 0 ? messageText.slice(0, 30) + (messageText.length > 30 ? "..." : "") : chat.title
          return { ...chat, messages: updatedMessages, title }
        }
        return chat
      }),
    )

    setIsLoading(true)
    setIsStreaming(true)

    // Crear AbortController para cancelar la solicitud
    abortControllerRef.current = new AbortController()

    // Crear mensaje de AI vacío que se irá llenando
    const aiMessageId = Date.now() + 1
    const aiMessage = {
      id: aiMessageId,
      text: "",
      sender: "ai",
      timestamp: new Date(),
      isStreaming: true,
    }

    setChats((prevChats) =>
      prevChats.map((chat) => {
        if (chat.id === currentChatId) {
          return { ...chat, messages: [...chat.messages, aiMessage] }
        }
        return chat
      }),
    )

    try {
      // Detectar si hay imágenes o PDFs
      const hasImages = attachments.some(att => att.type === "image")
      const hasPdf = pdfFile !== null
      
      let url = `${API_URL}/chat`
      let fetchOptions = { method: "POST" }
      
      if (hasImages || hasPdf) {
        // Enviar con FormData para imágenes y/o PDFs
        const formData = new FormData()
        formData.append('message', messageText)
        
        // Agregar imágenes
        for (const att of attachments) {
          if (att.type === "image") {
            // Convertir data URL a Blob
            const base64Response = await fetch(att.data)
            const blob = await base64Response.blob()
            formData.append('images', blob, att.name)
          }
        }
        
        // Agregar PDF si existe
        if (hasPdf) {
          formData.append('pdf', pdfFile, pdfFile.name)
        }
        
        fetchOptions.body = formData
      } else {
        // Enviar JSON para solo texto
        let messageContent = messageText
        
        // Si hay archivos de texto, incluirlos en el mensaje
        if (attachments.length > 0) {
          const textAttachments = attachments
            .filter(att => att.type === "text")
            .map(att => `[Archivo: ${att.name}]\n${att.data}`)
            .join("\n\n")
          
          messageContent = `${messageText}\n\n${textAttachments}`
        }
        
        fetchOptions.headers = { "Content-Type": "application/json" }
        fetchOptions.body = JSON.stringify({ message: messageContent })
      }

      // Agregar signal para abortar
      fetchOptions.signal = abortControllerRef.current.signal

      const response = await fetch(url, fetchOptions)
      
      // Procesar streaming
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""
      let fullText = ""

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        
        // Guardar la última línea incompleta
        buffer = lines.pop() || ""
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.error) {
                throw new Error(data.error)
              }
              
              if (data.chunk) {
                fullText += data.chunk
                
                // Actualizar el mensaje de AI progresivamente
                setChats((prevChats) =>
                  prevChats.map((chat) => {
                    if (chat.id === currentChatId) {
                      return {
                        ...chat,
                        messages: chat.messages.map((msg) =>
                          msg.id === aiMessageId
                            ? { ...msg, text: fullText, isStreaming: true }
                            : msg
                        ),
                      }
                    }
                    return chat
                  }),
                )
              }
              
              if (data.done) {
                // Finalizar streaming
                setChats((prevChats) =>
                  prevChats.map((chat) => {
                    if (chat.id === currentChatId) {
                      return {
                        ...chat,
                        messages: chat.messages.map((msg) =>
                          msg.id === aiMessageId
                            ? { ...msg, isStreaming: false }
                            : msg
                        ),
                      }
                    }
                    return chat
                  }),
                )
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError)
            }
          }
        }
      }
    } catch (error) {
      // Si fue cancelado por el usuario, no mostrar error
      if (error.name === 'AbortError') {
        console.log('Solicitud cancelada por el usuario')
        
        // Actualizar el mensaje con indicador de cancelación
        setChats((prevChats) =>
          prevChats.map((chat) => {
            if (chat.id === currentChatId) {
              return {
                ...chat,
                messages: chat.messages.map((msg) =>
                  msg.id === aiMessageId
                    ? { 
                        ...msg, 
                        text: msg.text || "Respuesta cancelada.", 
                        isStreaming: false,
                        isCancelled: true 
                      }
                    : msg
                ),
              }
            }
            return chat
          }),
        )
      } else {
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
      }
    } finally {
      setIsLoading(false)
      setIsStreaming(false)
      abortControllerRef.current = null
    }
  }

  const handleCancelResponse = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
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
      <Header theme={theme} onToggleTheme={toggleTheme} />

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
                {isStreaming && (
                  <div className="cancel-button-container">
                    <button onClick={handleCancelResponse} className="cancel-response-btn">
                      ✕ Cancelar respuesta
                    </button>
                  </div>
                )}
                {isLoading && !isStreaming && (
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
