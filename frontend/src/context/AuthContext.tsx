// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.4)
//
// TODO: Create React context for authentication state.
//
// AuthContext should provide:
//   - user: User | null (current logged-in user)
//   - token: string | null (JWT access token)
//   - isAuthenticated: boolean (derived from user !== null)
//   - login(token: string, user: User): void
//       - Save token to localStorage
//       - Set user and token in state
//   - logout(): void
//       - Remove token from localStorage
//       - Set user and token to null
//   - loading: boolean (true while checking localStorage on mount)
//
// AuthProvider component:
//   - On mount, check localStorage for existing token
//   - If token exists, decode it (or validate via API) to restore user state
//   - Wrap children in AuthContext.Provider
//
// Export:
//   - AuthContext
//   - AuthProvider
//   - useAuth hook (see hooks/useAuth.ts)
import React, { createContext, useState, useEffect, ReactNode } from "react"
import { User } from "../types"

interface AuthContextType {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    login: (token: string, user: User) => void
    logout: () => void
    loading: boolean
}
export const AuthContext = createContext<AuthContextType>({
    user: null,
    token: null,
    isAuthenticated: false,
    login: () => {},
    logout: () => {},
    loading: true,
})
interface AuthProviderProps {
    children: ReactNode
}
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null) 
    const [token, setToken] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)
    useEffect(() => {
    const storedToken = localStorage.getItem("access_token")
    if (storedToken) {
      // TODO: replace with real token decode or /auth/me API call
      setUser({
        id: 0,
        email: "",
        name: "",
        is_verified: false,
        created_at: "",
      })
      setToken(storedToken)
    }
    setLoading(false)
  }, [])
    const login = (token: string, user: User) => {
        localStorage.setItem("access_token", token)
        setUser(user)
        setToken(token)
    }
    const logout = () => {
        localStorage.removeItem("access_token")
        setUser(null)
        setToken(null)
    }
    return (
        <AuthContext.Provider value={{ user, token, isAuthenticated: !!user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    )
}
