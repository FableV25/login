import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { accessToken, refreshToken } from '../constants'

function Logout() {
    const navigate = useNavigate()

    useEffect(() => {
        localStorage.removeItem(accessToken)
        localStorage.removeItem(refreshToken)

        navigate('/login')
    }, [navigate])

    return (
        <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh' 
        /*might make it its own css file*/
        }}> 
            <p>Cerrando sesioneishon...</p>
        </div>
    )
}

export default Logout