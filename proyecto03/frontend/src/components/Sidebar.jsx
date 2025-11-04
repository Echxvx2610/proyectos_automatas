// Sidebar.jsx
import { Plus, MessageSquare, Trash2, Menu, X } from 'lucide-react'
import { useState } from "react"
import "./Sidebar.css"

function Sidebar({ chats, currentChatId, onNewChat, onSelectChat, onDeleteChat, isMobile }) {
  const [isOpen, setIsOpen] = useState(!isMobile)

  const toggleSidebar = () => setIsOpen(!isOpen)

  return (
    <>
      {isMobile && (
        <button className="sidebar-toggle" onClick={toggleSidebar} aria-label="Toggle sidebar">
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      )}

      <aside className={`sidebar ${isOpen ? "sidebar-open" : "sidebar-closed"}`}>
        <div className="sidebar-header">
          <button className="new-chat-button" onClick={onNewChat}>
            <Plus size={20} />
            <span>Nuevo Chat</span>
          </button>
        </div>

        <div className="sidebar-divider"></div>

        <div className="chats-list">
          {chats.length === 0 ? (
            <div className="empty-chats">
              <MessageSquare size={32} />
              <p>No hay chats aún</p>
            </div>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                className={`chat-item ${currentChatId === chat.id ? "chat-item-active" : ""}`}
                onClick={() => onSelectChat(chat.id)}
              >
                <MessageSquare size={18} className="chat-icon" />
                <div className="chat-item-content">
                  <div className="chat-item-title">{chat.title}</div>
                  <div className="chat-item-preview">{chat.messages.length} mensajes</div>
                </div>
                <button
                  className="delete-chat-button"
                  onClick={(e) => {
                    e.stopPropagation()
                    onDeleteChat(chat.id)
                  }}
                  aria-label="Delete chat"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>
    </>
  )
}

export default Sidebar