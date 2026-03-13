// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Login page.
//
// Form fields:
//   - Email (email input, required)
//   - Password (password input, required)
//
// Behavior:
//   1. On submit, call api/auth.ts login({ email, password })
//   2. On success:
//      - Call auth context's login(token, user) to store JWT and user
//      - Redirect to / (BrowsePage)
//   3. On 401 error: show "Invalid email or password"
//   4. On 403 error: show "Please verify your email first" with link to /verify
//   5. Show loading spinner while request is in flight
//
// Styling: Use YU branding (red #E31837 for submit button)
// Links:
//   - "Don't have an account? Register" -> /register
//   - "Need to verify your email?" -> /verify
import { useState } from "react";
import { useNavigate} from "react-router-dom";
import { login as apiLogin } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import "../styles/global.css"

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token, user } = await apiLogin({ email, password });
      login(access_token, user);
      navigate("/");
    } catch (err: any) {
      if (err?.response?.status === 401) setError("Invalid email or password");
      else if (err?.response?.status === 403) setError("Please verify your email first.");
      else setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
  <div className="auth-card">
    <h1 className="auth-title">YUTrade</h1>
    <form className="auth-form" onSubmit={handleSubmit}>
      <div className="auth-field">
        <label className="auth-label">Email</label>
        <input className="auth-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
  required />
      </div>
      <div className="auth-field">
        <label className="auth-label">Password</label>
        <input
  className="auth-input"
  type="password"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  required
/>
      </div>
      {error && <p className="auth-error">{error}</p>}
      <button className="btn-red" type="button" onClick={() => navigate("/register")}>
        Create a New Account
      </button>
      <button className="btn-outline" type="submit">Login</button>
    </form>
  </div>
</div>
  );
}
