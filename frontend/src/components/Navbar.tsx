// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.7)
//
// TODO: Navigation bar with YU branding.
//
// Structure:
//   <nav className="navbar">
//     <Link to="/" className="navbar-brand">YU Trade</Link>
//     <div className="navbar-links">
//       {/* Always visible */}
//       <Link to="/">Browse</Link>
//
//       {/* Visible when logged in */}
//       <Link to="/create">Sell Item</Link>
//       <Link to="/my-listings">My Listings</Link>
//       <Link to="/messages">Messages</Link>
//       <span>Hello, {user.name}</span>
//       <button onClick={logout}>Logout</button>
//
//       {/* Visible when NOT logged in */}
//       <Link to="/login">Login</Link>
//       <Link to="/register">Register</Link>
//     </div>
//   </nav>
//
// Behavior:
//   - Use useAuth() hook to check isAuthenticated and get user/logout
//   - Conditionally render links based on auth state
//
// Styling:
//   - Background: YU red (#E31837) or white with red accents
//   - Text/links: white (on red bg) or dark (on white bg)
//   - Horizontal layout, logo left, links right
//   - Responsive: hamburger menu on mobile (optional stretch goal)
