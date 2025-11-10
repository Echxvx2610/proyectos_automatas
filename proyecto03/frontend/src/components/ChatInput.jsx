import { useState, useEffect, useRef } from "react"
import { Send, Mic, MicOff } from "lucide-react"
import "./ChatInput.css"

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("")
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
      <form onSubmit={handleSubmit} className="chat-input-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isListening ? "Escuchando..." : "Escribe tu pregunta aquí..."}
          disabled={disabled || isListening}
          rows={1}
          className="chat-input"
        />
        
        {/* Botón de micrófono */}
        <button 
          type="button"
          onClick={toggleListening}
          disabled={disabled}
          className={`voice-button ${isListening ? 'listening' : ''}`}
          title={isListening ? "Detener grabación" : "Hablar"}
        >
          {isListening ? <MicOff size={20} /> : <Mic size={20} />}
        </button>

        {/* Botón de enviar */}
        <button 
          type="submit" 
          disabled={disabled || !input.trim()} 
          className="send-button"
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
          <>Presiona Enter para enviar, Shift + Enter para nueva línea</>
        )}
      </div>
    </div>
  )
}

export default ChatInput