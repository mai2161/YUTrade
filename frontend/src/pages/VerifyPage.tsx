// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Email verification page.
//
// User arrives here after registration with email in URL query param.
//
// Form fields:
//   - Email (pre-filled from query param, read-only or editable)
//   - Verification Code (text input, 6 digits)
//
// Behavior:
//   1. Read email from URL: new URLSearchParams(location.search).get("email")
//   2. On submit, call api/auth.ts verify({ email, code })
//   3. On success: show success message, redirect to /login after 2 seconds
//   4. On error: show "Invalid or expired verification code"
//   5. Show loading spinner while request is in flight
//
// Styling: Simple centered form with YU branding
import { useState, useEffect, useRef } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { verify } from "../api/auth"

const CODE_LENGTH = 5
const RESEND_SECONDS = 60

export default function VerifyPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const email = new URLSearchParams(location.search).get("email") || ""

  const [digits, setDigits] = useState<string[]>(Array(CODE_LENGTH).fill(""))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [countdown, setCountdown] = useState(RESEND_SECONDS)
  const inputRefs = useRef<(HTMLInputElement | null)[]>([])

  useEffect(() => {
    if (countdown <= 0) return
    const t = setTimeout(() => setCountdown((c) => c - 1), 1000)
    return () => clearTimeout(t)
  }, [countdown])

  const handleChange = (i: number, val: string) => {
    if (!/^\d?$/.test(val)) return
    const next = [...digits]
    next[i] = val
    setDigits(next)
    if (val && i < CODE_LENGTH - 1) inputRefs.current[i + 1]?.focus()
  }

  const handleKeyDown = (i: number, e: React.KeyboardEvent) => {
    if (e.key === "Backspace" && !digits[i] && i > 0)
      inputRefs.current[i - 1]?.focus()
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, CODE_LENGTH)
    if (!pasted) return
    e.preventDefault()
    const next = [...digits]
    pasted.split("").forEach((ch, i) => { next[i] = ch })
    setDigits(next)
    inputRefs.current[Math.min(pasted.length, CODE_LENGTH - 1)]?.focus()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const code = digits.join("")
    if (code.length < CODE_LENGTH) return
    setError("")
    setLoading(true)
    try {
      await verify({ email, code })
      navigate("/login")
    } catch {
      setError("Invalid or expired verification code")
    } finally {
      setLoading(false)
    }
  }

  const handleResend = () => {
    // TODO: call resend API when available
    setCountdown(RESEND_SECONDS)
  }

  const fmt = (s: number) =>
    `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`

  return (
    <div className="verify-page">
      <div className="verify-card">
        <span className="yu-logo">YUTrade</span>
        <h1 className="auth-title">Verify Email</h1>
        <p style={{ fontSize: 12, color: '#666', textAlign: 'center', marginBottom: 8 }}>
          We've sent a 5-digit verification code to your YorkU email.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label className="auth-label">Enter Verification Code</label>
            <div className="verify-boxes" onPaste={handlePaste}>
              {digits.map((d, i) => (
                <input
                  key={i}
                  ref={(el) => { inputRefs.current[i] = el }}
                  className="verify-box"
                  type="text"
                  inputMode="numeric"
                  maxLength={1}
                  value={d}
                  onChange={(e) => handleChange(i, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(i, e)}
                />
              ))}
            </div>
          </div>

          {error && <p className="auth-error">{error}</p>}

          <p className="verify-countdown">
            {countdown > 0 ? `Resend Code in ${fmt(countdown)}` : "You can resend now"}
          </p>

          <button
            type="button"
            className="btn-red"
            onClick={handleResend}
            disabled={countdown > 0}
          >
            Resend Code
          </button>

          <button
            type="submit"
            className="btn-red"
            disabled={loading || digits.join("").length < CODE_LENGTH}
          >
            {loading ? "Verifying…" : "Verify"}
          </button>
        </form>
      </div>
    </div>
  )
}