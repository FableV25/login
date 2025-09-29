import { useState } from 'react'
import api from '../utils/api'
import { useNavigate, Link } from 'react-router-dom'
import { accessToken, refreshToken } from '../constants'

import "../styles/Form.css"
import LoadingIndicator from './LoadingInd'

function Form({ route, method, showRegisterLink, showLoginLink }) {        
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method === "login" ? "login" : "register"

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, {username, password})
            if (method === "login") {
                localStorage.setItem(accessToken, res.data.access)
                localStorage.setItem(refreshToken, res.data.refresh)
                navigate('/')
            } else {
                navigate('/login')
            }

        } catch (error) {

            alert(error)

        } finally {

            setLoading(false)
            
        }   
    }

    return (
        <form onSubmit={handleSubmit} className='form-container'>
            <h1>{name}</h1>
            <input 
                className='form-input'
                type='text'   
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder='Username'
            /> 

            <input 
                className='form-input'
                type='password'   
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='Password'
            /> 

            {loading && <LoadingIndicator/>}

            <button className='form-button' type='submit'> 
                {name}
            </button>

            {showRegisterLink && (
                <p>
                    <Link to="/register">Crear un usuario</Link>
                </p>
            )}

            {showLoginLink && (
                <p>
                    <Link to="/login">Iniciar sesión</Link>
                </p>
            )}

        </form>
    )
}

export default Form
