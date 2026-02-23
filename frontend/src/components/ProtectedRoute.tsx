// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.4)
//
// TODO: Route wrapper that redirects unauthenticated users to login.
//
// Props:
//   - children: React.ReactNode
//
// Behavior:
//   1. Use the useAuth() hook to get { isAuthenticated, loading }
//   2. If loading is true: show a loading spinner (auth state is being restored)
//   3. If not authenticated: redirect to /login using <Navigate to="/login" replace />
//   4. If authenticated: render {children}
//
// Usage in App.tsx:
//   <Route path="/create" element={
//     <ProtectedRoute>
//       <CreateListingPage />
//     </ProtectedRoute>
//   } />
