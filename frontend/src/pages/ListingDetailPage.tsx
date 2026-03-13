// Assigned to: Mai Komar
// Phase: 2 (F2.4)

import React, { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { getListing } from "../api/listings"
import { Listing } from "../types"

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

function StarRating({ rating, max = 5 }: { rating: number; max?: number }) {
  return (
    <div className="star-row">
      {Array.from({ length: max }).map((_, i) => {
        const filled = i < Math.floor(rating)
        const half = !filled && i < rating
        return (
          <span
            key={i}
            className={filled ? "star-icon" : half ? "star-icon-half" : "star-icon-empty"}
          >
            ★
          </span>
        )
      })}
    </div>
  )
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return "Posted today"
  if (days === 1) return "Posted 1 day ago"
  return `Posted ${days} days ago`
}

export default function ListingDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [listing, setListing] = useState<Listing | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [imgIdx, setImgIdx] = useState(0)

  useEffect(() => {
    if (!id) return
    getListing(parseInt(id))
      .then(setListing)
      .catch(() => setError("Listing not found"))
      .finally(() => setLoading(false))
  }, [id])

  const header = (
    <div className="app-header">
      <button className="app-header-btn" onClick={() => navigate(-1)}>
        ←
      </button>
      <span className="app-header-title">Listing Details</span>
      <button className="app-header-btn" onClick={() => navigate("/my-listings")}>
        👤
      </button>
    </div>
  )

  if (loading) {
    return (
      <div className="app-screen">
        {header}
        <div className="app-content" style={{ textAlign: "center", paddingTop: 48, color: "#aaa" }}>
          Loading…
        </div>
      </div>
    )
  }

  if (error || !listing) {
    return (
      <div className="app-screen">
        {header}
        <div className="app-content" style={{ textAlign: "center", paddingTop: 48 }}>
          <p style={{ color: "#888" }}>{error || "Listing not found"}</p>
        </div>
      </div>
    )
  }

  const images = [...listing.images].sort((a, b) => a.position - b.position)
  const currentImg = images[imgIdx]

  return (
    <div className="app-screen">
      {header}
      <div className="app-content">
        {/* Two-column: carousel + details */}
        <div className="listing-detail-cols">
          {/* Left: Image Carousel */}
          <div className="carousel-wrap">
            <div className="carousel-img">
              {currentImg ? (
                <img
                  src={`${API_URL}/${currentImg.file_path}`}
                  alt={listing.title}
                />
              ) : (
                <span className="carousel-img-placeholder">🖼</span>
              )}
            </div>
            {images.length > 1 && (
              <div className="carousel-dots">
                {images.map((_, i) => (
                  <button
                    key={i}
                    className={`carousel-dot${i === imgIdx ? " active" : ""}`}
                    onClick={() => setImgIdx(i)}
                  />
                ))}
              </div>
            )}
            {images.length === 0 && (
              <div className="carousel-dots">
                <button className="carousel-dot active" />
                <button className="carousel-dot" />
                <button className="carousel-dot" />
              </div>
            )}
          </div>

          {/* Right: Title, Description, Fields */}
          <div>
            <div className="detail-title">{listing.title}</div>
            <textarea
              className="detail-desc"
              readOnly
              value={listing.description || ""}
              placeholder="No description"
            />
            <div className="detail-field-group">
              <div className="detail-label">Listed Price</div>
              <div className="detail-value">${listing.price.toFixed(2)}</div>
            </div>
            <div className="detail-field-group">
              <div className="detail-label">Category</div>
              <div className="detail-value">{listing.category || "—"}</div>
            </div>
            <div className="detail-field-group">
              <div className="detail-label">Condition</div>
              <div className="detail-value">—</div>
            </div>
          </div>
        </div>

        {/* Posted By Section */}
        <div className="posted-by-section">
          <div className="posted-by-grid">
            <div>
              <div className="detail-label" style={{ marginBottom: 4 }}>Posted By</div>
              <div className="detail-value" style={{ marginBottom: 8 }}>
                {listing.seller.name}
              </div>
              <div className="detail-label" style={{ marginBottom: 4 }}>Seller Rating</div>
              <StarRating rating={3.5} />
            </div>
            <div style={{ paddingTop: 20 }}>
              <button
                className="btn-red-sm"
                onClick={() => navigate(`/seller/${listing.seller_id}`)}
              >
                View Seller Profile
              </button>
              <button
                className="btn-red-sm"
                onClick={() => navigate("/messages")}
              >
                Message Seller
              </button>
            </div>
          </div>
          <div className="timestamp-text">{timeAgo(listing.created_at)}</div>
        </div>
      </div>
    </div>
  )
}
