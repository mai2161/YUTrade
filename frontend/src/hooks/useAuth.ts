// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.4)
//
// TODO: Custom hook to access auth context.
//
// import { useContext } from "react"
// import { AuthContext } from "../context/AuthContext"
//
// export function useAuth() {
//   const context = useContext(AuthContext)
//   if (!context) {
//     throw new Error("useAuth must be used within an AuthProvider")
//   }
//   return context
// }
//
// This hook provides a clean way for components to access:
//   const { user, token, isAuthenticated, login, logout, loading } = useAuth()
