import React from "react"
import "../styles/Note.css"
import { formatDate } from "../config/Date"

function Note({ note, onDelete, showDeleteButton, currentUserId }) {
    const formattedDate = formatDate(note.created_at)
    const isOwnNote = currentUserId === note.author_id

    return (
        <div className="note-container">
            <div className="note-header">
                <p className="note-title">{note.title}</p>
                <div className="note-meta">
                    <span className="note-author">
                        De: {note.author_username} {isOwnNote && "(You)"}
                    </span>
                    <span className="note-date">{formattedDate}</span>
                </div>
            </div>
            
            <p className="note-content">{note.content}</p>
            
            <div className="note-actions">
                {showDeleteButton && (
                    <button 
                        className="delete-button" 
                        onClick={() => onDelete(note.id)}
                        title="Only administrators can delete notes"
                    >
                        Eliminar nota
                    </button>
                )}
            </div>
        </div>
    )
} 

export default Note