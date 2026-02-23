// Assigned to: Mai Komar
// Phase: 1 (F1.6)
//
// TODO: Main App component with routing and auth context.
//
// 1. Import BrowserRouter, Routes, Route from "react-router-dom"
// 2. Import AuthProvider from "./context/AuthContext"
// 3. Import Layout from "./components/Layout"
// 4. Import ProtectedRoute from "./components/ProtectedRoute"
// 5. Import all page components
//
// 6. Define routes:
//    /register        -> RegisterPage
//    /verify          -> VerifyPage
//    /login           -> LoginPage
//    /                -> BrowsePage (public, default home page)
//    /listings/:id    -> ListingDetailPage (public)
//    /create          -> CreateListingPage (protected)
//    /my-listings     -> MyListingsPage (protected)
//    /messages        -> MessagesPage (protected)
//
// 7. Wrap everything in:
//    <AuthProvider>
//      <BrowserRouter>
//        <Layout>
//          <Routes>...</Routes>
//        </Layout>
//      </BrowserRouter>
//    </AuthProvider>
//
// 8. Protected routes should use <ProtectedRoute> wrapper that
//    redirects to /login if user is not authenticated
