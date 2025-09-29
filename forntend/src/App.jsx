import react from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

import Home from './pages/home'
import Login from './pages/login'
import Register from './pages/register'
import NotFound from './pages/notFound'
import Logout from './pages/logout'
import ProtectedRoute from './components/protectedRoute'

function RegisterAndLogOut() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
      <BrowserRouter> 
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />

          <Route 
            path='/login' 
            element={<Login />}>
          </Route>

          <Route 
            path='/logout' 
            element={<Logout />}>
          </Route>

          <Route 
            path='/register' 
            element={<RegisterAndLogOut />}>
          </Route>

          <Route 
            path="*" 
            element={<NotFound />}>
          </Route>

        </Routes> 
      </BrowserRouter>
  )
}

export default App