// Phase: 2 (F2.5)
// Seller profile view — shows seller info and all their listings.

import React, { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { getListings } from "../api/listings"
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

export default function SellerProfilePage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [listings, setListings] = useState<Listing[]>([])
  const [loading, setLoading] = useState(true)
  const [sellerName, setSellerName] = useState("")

  useEffect(() => {
    getListings({})
      .then((data) => {
        const all: Listing[] = data.listings || []
        const sellerId = parseInt(id || "0")
        const sellerListings = all.filter((l) => l.seller_id === sellerId)
        setListings(sellerListings)
        if (sellerListings.length > 0) {
          setSellerName(sellerListings[0].seller.name)
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [id])

  return (
    <div className="app-screen">
      <div className="app-header">
        <button className="app-header-btn" onClick={() => navigate(-1)}>
          ←
        </button>
        <span className="app-header-title">Seller Profile Page</span>
        <button className="app-header-btn" onClick={() => navigate("/my-listings")}>
          👤
        </button>
      </div>

      <div className="app-content">
        {/* Profile Top Section */}
        <div className="seller-profile-top">
          <div className="seller-avatar">
            <span style={{ fontSize: 36, color: "#bbb" }}>👤</span>
          </div>
          <div className="seller-info-col">
            <input
              className="seller-name-input"
              readOnly
              value={sellerName}
              placeholder="Seller Name"
            />
            <div className="seller-rating-row">
              <span>Rating</span>
              <StarRating rating={4} />
            </div>
            <div className="seller-joined">Joined in 2017</div>
            <button
              className="btn-red"
              style={{ width: "auto", padding: "7px 16px", fontSize: 12 }}
              onClick={() => navigate("/messages")}
            >
              Message Seller
            </button>
          </div>
        </div>

        {/* All Seller Listings */}
        <div className="all-listings-title">All Seller Listings</div>
        {loading ? (
          <p style={{ textAlign: "center", color: "#aaa", paddingTop: 24 }}>Loading…</p>
        ) : listings.length === 0 ? (
          <p style={{ textAlign: "center", color: "#aaa", paddingTop: 24 }}>
            No listings found.
          </p>
        ) : (
          <div className="listings-table-wrap">
            <table className="listings-table">
              <tbody>
                {listings.map((listing) => {
                  const firstImg = [...listing.images].sort(
                    (a, b) => a.position - b.position
                  )[0]
                  return (
                    <tr key={listing.id}>
                      <td>
                        <div className="listing-thumb">
                          {firstImg ? (
                            <img
                              src={`${API_URL}/${firstImg.file_path}`}
                              alt={listing.title}
                              style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: 4, display: "block" }}
                            />
                          ) : (
                            <span style={{ color: "#ccc", fontSize: 18 }}>🖼</span>
                          )}
                        </div>
                      </td>
                      <td style={{ maxWidth: 80, wordBreak: "break-word" }}>
                        {listing.title}
                      </td>
                      <td>${listing.price.toFixed(2)}</td>
                      <td>{listing.category || "—"}</td>
                      <td>
                        <span
                          className={`status-pill ${
                            listing.status === "active"
                              ? "status-pill-active"
                              : listing.status === "sold"
                              ? "status-pill-sold"
                              : "status-pill-inactive"
                          }`}
                        >
                          {listing.status === "active"
                            ? "Active"
                            : listing.status === "sold"
                            ? "Sold"
                            : "Inactive"}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn-table-action"
                          onClick={() => navigate(`/listings/${listing.id}`)}
                        >
                          View Listing
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
