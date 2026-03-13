// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Registration page for new users.
//
// Form fields:
//   - Name (text input, required)
//   - Email (email input, required — must be @my.yorku.ca or @yorku.ca)
//   - Password (password input, required, min 8 characters)
//   - Confirm Password (must match)
//
// Behavior:
//   1. Validate email domain on client side before submitting
//      (show error if not a YorkU email)
//   2. Validate passwords match
//   3. On submit, call api/auth.ts register()
//   4. On success: redirect to /verify?email={email} so user can enter code
//   5. On error (409 duplicate): show "Email already registered"
//   6. On error (400 bad domain): show "Must use a YorkU email"
//   7. Show loading spinner while request is in flight
//
// Styling: Use YU branding (red #E31837 for buttons, clean form layout)
// Link: "Already have an account? Log in" -> /login

import React, { useState } from "react"
import {useNavigate } from "react-router-dom"
import { register } from "../api/auth"

const RegisterPage: React.FC = () => {
    const navigate = useNavigate()
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const validateEmail = (email: string) => {
        const domain = email.split("@")[1]
        return domain === "my.yorku.ca" || domain === "yorku.ca"
    }
    const validatePassword = (pwd: string): string => {
        if (pwd.length < 8) return "Password must be at least 8 characters"
        return ""
    }
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        if (!validateEmail(email)) {
            setError("Must use a YorkU email (@my.yorku.ca or @yorku.ca)")
            return
        }
        const pwdError = validatePassword(password)
        if (pwdError) {
            setError(pwdError)
            return
        }
        if (password !== confirmPassword) {
            setError("Passwords do not match")
            return
        }
        setLoading(true)
        try {
            await register({ name, email, password })
            navigate(`/verify?email=${encodeURIComponent(email)}`)
        } catch (err: any) {
            if (err.response?.status === 409) {
                setError("Email already registered")
            } else if (err.response?.status === 400) {
                setError("Must use a YorkU email")
            } else {
                setError("Registration failed")
            }
        } finally {
            setLoading(false)
        }
    }
     return (
    <div className="auth-page">
      <div className="auth-card">
        <span className="yu-logo">YUTrade</span>
        <h1 className="auth-title">Create Account</h1>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label className="auth-label">Full Name</label>
            <input
              className="auth-input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">YorkU Email</label>
            <input
              className="auth-input"
              type="email"
              placeholder="you@my.yorku.ca"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Password</label>
            <input
              className="auth-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Confirm Password</label>
            <input
              className="auth-input"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button className="btn-red" type="submit" disabled={loading}>
            {loading ? "Registering…" : "Register"}
          </button>
           <label className="reg-text">Already have an existing account?</label>
        <button className="btn-outline" type="button" onClick={() => navigate("/login")}>
             Login
       </button> 
        </form>
      </div>
    </div>
  )
}

export default RegisterPage