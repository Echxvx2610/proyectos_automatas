import { useState, useRef, useEffect, useRef } from "react"
import { Send, Paperclip, X, FileText, ImageIcon, Mic, MicOff } from "lucide-react"
import "./ChatInput.css"

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("")
  const [attachments, setAttachments] = useState([])
  const [isDragging, setIsDragging] = useState(false)
  const [previewImage, setPreviewImage] = useState(null)
  const fileInputRef = useRef(null)
  const [isListening, setIsListening] = useState(false)
  const [browserSupported, setBrowserSupported] = useState(true)
  const recognitionRef = useRef(null)

  // Verificar soporte del navegador
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    
    if (!SpeechRecognition) {
      setBrowserSupported(false)
      console.warn("Tu navegador no soporta reconocimiento de voz. Usa Chrome o Edge.")
      return
    }

    // Inicializar reconocimiento de voz
    const recognition = new SpeechRecognition()
    recognition.continuous = false // Se detiene automáticamente
    recognition.interimResults = true // Mostrar resultados mientras habla
    recognition.lang = 'es-ES' // Español

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

  const toggleListening = () => {
    if (!browserSupported) {
      alert("Tu navegador no soporta reconocimiento de voz. Usa Google Chrome o Microsoft Edge.")
      return
    }

    if (isListening) {
      // Detener grabación
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      // Iniciar grabación
      try {
        recognitionRef.current?.start()
        setIsListening(true)
      } catch (error) {
        console.error('Error al iniciar reconocimiento:', error)
      }
    }
  }

  return (
  <div className="chat-input-container">
    {/* Vista previa de archivos adjuntos */}
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
                  onClick={() => setPreviewImage(att.data)} // abrir vista previa
                />
                <ImageIcon size={16} />
              </>
            ) : (
              <>
                <FileText size={16} />
                <button
                  type="button"
                  className="preview-text-btn"
                  onClick={() =>
                    alert(att.data.slice(0, 500) + (att.data.length > 500 ? "..." : ""))
                  }
                >
                  Ver contenido
                </button>
              </>
            )}
            <span className="attachment-name">{att.name}</span>
            <button
              type="button"
              onClick={() => removeAttachment(att.id)}
              className="remove-attachment"
            >
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    )}

    {/* Formulario del input de chat */}
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
      >
        <Paperclip size={20} />
      </button>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Escribe tu pregunta aquí..."
        disabled={disabled}
        rows={1}
        className="chat-input"
      />

      <button
        type="submit"
        disabled={disabled || (!input.trim() && attachments.length === 0)}
        className="send-button"
      >
        <Send size={20} />
      </button>
    </form>

    <div className="input-hint">
      Presiona Enter para enviar, Shift + Enter para nueva línea • Arrastra archivos para adjuntar
    </div>

    {/* Modal de vista previa de imagen */}
    {previewImage && (
      <div className="image-preview-modal" onClick={() => setPreviewImage(null)}>
        <img
          src={previewImage}
          alt="Vista previa"
          className="image-preview-large"
        />
      </div>
    )}
  </div>
)

}

export default ChatInput