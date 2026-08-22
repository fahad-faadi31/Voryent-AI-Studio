import { Link, useNavigate } from 'react-router-dom'
import { isAuthenticated, clearToken } from '../utils/auth'

export default function Navbar() {
  const navigate = useNavigate()
  const authenticated = isAuthenticated()

  function handleLogout() {
    clearToken()
    navigate('/')
  }

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-voryent-600">
          Voryent AI Studio
        </Link>

        <div className="flex items-center gap-4">
          {authenticated ? (
            <>
              <Link
                to="/studio"
                className="text-gray-700 hover:text-voryent-600"
              >
                Studio
              </Link>

              <Link
                to="/history"
                className="text-gray-700 hover:text-voryent-600"
              >
                History
              </Link>

              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-voryent-600"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-gray-700 hover:text-voryent-600"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="bg-voryent-600 text-white px-4 py-2 rounded-md hover:bg-voryent-700"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}