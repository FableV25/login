import { Link } from 'react-router-dom'
import '../styles/NotFound.css'

function NotFound() {
    return (
        <div className="not-found-container">
            <div className="not-found-content">
                <h1 className="error-code">404</h1>
                <h2 className="error-title">Pagina no encontrada</h2>
                <p className="error-message">
                    La pagina a la que estásestas intentado acceder no existe o ha sido movida.
                </p>
                <Link to="/" className="home-button">
                    Volver al Inicio
                </Link>
            </div>
        </div>
    )
}

export default NotFound