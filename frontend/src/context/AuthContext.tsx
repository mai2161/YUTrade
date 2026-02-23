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
