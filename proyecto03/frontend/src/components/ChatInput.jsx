"use client"
import { useState, useRef, useEffect } from "react"
import { Send, Paperclip, X, FileText, Image, Mic, MicOff } from "lucide-react"
import "./ChatInput.css"

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("")
  const [attachments, setAttachments] = useState([])
  const [isDragging, setIsDragging] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [browserSupported, setBrowserSupported] = useState(true)
  const [previewImage, setPreviewImage] = useState(null)
  const [previewText, setPreviewText] = useState(null)
  const fileInputRef = useRef(null)
  const recognitionRef = useRef(null)

  // Verificar soporte del navegador para reconocimiento de voz
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    
    if (!SpeechRecognition) {
      setBrowserSupported(false)
      console.warn("Tu navegador no soporta reconocimiento de voz. Usa Chrome o Edge.")
      return
    }

    // Inicializar reconocimiento de voz
    const recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang = 'es-ES'

    // Evento: Cuando se recibe texto
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')
      
      setInput(transcript)
    }

    // Evento: Error
    recognition.onerror = (event) => {
      console.error('Error de reconocimiento:', event.error)
      setIsListening(false)
      
      if (event.error === 'not-allowed') {
        alert('Permiso de micrófono denegado. Por favor, permite el acceso al micrófono.')
      }
    }

    // Evento: Cuando termina de escuchar
    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if ((input.trim() || attachments.length > 0) && !disabled) {
      onSend(input, attachments)
      setInput("")
      setAttachments([])
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const toggleListening = () => {
    if (!browserSupported) {
      alert("Tu navegador no soporta reconocimiento de voz. Usa Google Chrome o Microsoft Edge.")
      return
    }

    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      try {
        recognitionRef.current?.start()
        setIsListening(true)
      } catch (error) {
        console.error('Error al iniciar reconocimiento:', error)
      }
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    processFiles(files)
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    processFiles(files)
  }

  const processFiles = (files) => {
    const validFiles = files.filter((file) => {
      const isImage = file.type.startsWith("image/")
      const isText = file.type.startsWith("text/") || file.name.endsWith(".txt")
      return isImage || isText
    })

    validFiles.forEach((file) => {
      const reader = new FileReader()

      if (file.type.startsWith("image/")) {
        reader.onload = (e) => {
          setAttachments((prev) => [
            ...prev,
            {
              id: Date.now() + Math.random(),
              type: "image",
              name: file.name,
              data: e.target.result,
            },
          ])
        }
        reader.readAsDataURL(file)
      } else {
        reader.onload = (e) => {
          setAttachments((prev) => [
            ...prev,
            {
              id: Date.now() + Math.random(),
              type: "text",
              name: file.name,
              data: e.target.result,
            },
          ])
        }
        reader.readAsText(file)
      }
    })
  }

  const removeAttachment = (id) => {
    setAttachments((prev) => prev.filter((att) => att.id !== id))
  }

  const handleImageClick = (imageData) => {
    setPreviewImage(imageData)
  }

  const handleTextPreview = (textData, fileName) => {
    setPreviewText({ data: textData, name: fileName })
  }

  return (
    <div className="chat-input-container">
      {/* Modal de vista previa de imagen */}
      {previewImage && (
        <div className="image-preview-modal" onClick={() => setPreviewImage(null)}>
          <img src={previewImage} alt="Preview" className="image-preview-large" />
        </div>
      )}

      {/* Modal de vista previa de texto */}
      {previewText && (
        <div className="image-preview-modal" onClick={() => setPreviewText(null)}>
          <div 
            style={{
              background: 'var(--bg-secondary)',
              padding: '2rem',
              borderRadius: '12px',
              maxWidth: '600px',
              maxHeight: '80vh',
              overflow: 'auto',
              color: 'var(--text-primary)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-primary)' }}>{previewText.name}</h3>
            <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', fontFamily: 'inherit' }}>
              {previewText.data}
            </pre>
          </div>
        </div>
      )}

      {attachments.length > 0 && (
        <div className="attachments-preview">
          {attachments.map((att) => (
            <div key={att.id} className="attachment-item">
              {att.type === "image" ? (
                <>
                  <img 
                    src={att.data || "/placeholder.svg"} 
                    alt={att.name} 
                    className="attachment-thumbnail"
                    onClick={() => handleImageClick(att.data)}
                    style={{ cursor: 'pointer' }}
                  />
                  <Image size={16} />
                </>
              ) : (
                <>
                  <FileText size={16} />
                  <button
                    type="button"
                    onClick={() => handleTextPreview(att.data, att.name)}
                    className="preview-text-btn"
                  >
                    ver
                  </button>
                </>
              )}
              <span className="attachment-name">{att.name}</span>
              <button type="button" onClick={() => removeAttachment(att.id)} className="remove-attachment">
                <X size={14} />
              </button>
            </div>
          ))}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className={`chat-input-form ${isDragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isDragging && (
          <div className="drag-overlay">
            <Paperclip size={32} />
            <p>Suelta los archivos aquí</p>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*,text/*,.txt"
          onChange={handleFileSelect}
          style={{ display: "none" }}
        />

        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="attach-button"
          disabled={disabled}
          title="Adjuntar archivo"
        >
          <Paperclip size={20} />
        </button>

        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isListening ? "Escuchando..." : "Escribe tu pregunta aquí..."}
          disabled={disabled || isListening}
          rows={1}
          className="chat-input"
        />

        <button
          type="button"
          onClick={toggleListening}
          disabled={disabled}
          className={`voice-button ${isListening ? 'listening' : ''}`}
          title={isListening ? "Detener grabación" : "Hablar"}
        >
          {isListening ? <MicOff size={20} /> : <Mic size={20} />}
        </button>

        <button
          type="submit"
          disabled={disabled || (!input.trim() && attachments.length === 0)}
          className="send-button"
          title="Enviar mensaje"
        >
          <Send size={20} />
        </button>
      </form>
      
      <div className="input-hint">
        {isListening ? (
          <span className="recording-hint">
            🔴 Grabando... Habla ahora
          </span>
        ) : (
          <>Presiona Enter para enviar, Shift + Enter para nueva línea • Arrastra archivos para adjuntar</>
        )}
      </div>
    </div>
  )
}

export default ChatInput