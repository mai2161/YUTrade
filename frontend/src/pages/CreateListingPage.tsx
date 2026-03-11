// Assigned to: Mai Komar
// Phase: 2 (F2.5)
//
// TODO: Create new listing page (protected — requires authentication).
//
// Form fields:
//   - Title (text input, required, max 200 chars)
//   - Description (textarea, optional)
//   - Price (number input, required, min 0.01)
//   - Category (dropdown select, optional)
//       Options: "Textbooks", "Electronics", "Furniture", "Clothing", "Other"
//   - Images (file input, multiple, optional — uses ImageUpload component)
//
// Behavior:
//   1. Build a FormData object on submit:
//      - Append title, description, price, category as form fields
//      - Append each selected image file as "images"
//   2. Call api/listings.ts createListing(formData)
//   3. On success: redirect to /listings/{newListing.id}
//   4. On error: show validation errors
//   5. Show loading spinner while submitting
//
// Validation:
//   - Title is required
//   - Price must be a positive number
//   - Images should be image files (jpg, png, gif, webp)
//   - Max file size: 5MB per image (client-side check)
import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { createListing } from "../api/listings"
import "../styles/global.css"
import ImageUpload from "../components/ImageUpload"

export default function CreateListingPage() {
  const navigate = useNavigate()
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [price, setPrice] = useState("")
  const [category, setCategory] = useState("")
  const [images, setImages] = useState<File[]>([])
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    if (!title.trim()) {
      setError("Title is required")
      return
    }
    const priceNum = parseFloat(price)
    if (isNaN(priceNum) || priceNum < 0.01) {
      setError("Price must be at least $0.01")
      return
    }
    const formData = new FormData()
    formData.append("title", title)
    formData.append("description", description)
    formData.append("price", price)
    if (category) formData.append("category", category)
    images.forEach((file) => formData.append("images", file))
    setLoading(true)
    try {
      const newListing = await createListing(formData)
      navigate(`/listings/${newListing.id}`)
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to create listing")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card listing-card">
        <h1 className="auth-title">Create Listing</h1>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label className="auth-label">Title *</label>
            <input
              className="auth-input"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={200}
              required
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Description</label>
            <textarea
              className="auth-input listing-textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Price ($) *</label>
            <input
              className="auth-input"
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              min={0.01}
              step={0.01}
              required
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Category</label>
            <select
              className="auth-input listing-select"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="">-- Select Category --</option>
              <option value="Textbooks">Textbooks</option>
              <option value="Electronics">Electronics</option>
              <option value="Furniture">Furniture</option>
              <option value="Clothing">Clothing</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="auth-field">
            <label className="auth-label">Images</label>
            <ImageUpload images={images} onChange={setImages} />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button className="btn-red" type="submit" disabled={loading}>
            {loading ? "Creating…" : "Create Listing"}
          </button>

          <button className="btn-outline" type="button" onClick={() => navigate(-1)}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  )
}