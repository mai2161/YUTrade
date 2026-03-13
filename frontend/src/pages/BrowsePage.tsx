// Assigned to: Harnaindeep Kaur
// Phase: 2 (F2.3)

import React, { useState, useEffect, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { getListings } from "../api/listings"
import { Listing } from "../types"
import { AuthContext } from "../context/AuthContext"

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

const CATEGORIES = ["All", "Textbooks", "Electronics", "Furniture", "Clothing", "Other"]

export default function BrowsePage() {
  const navigate = useNavigate()
  const { user, logout, isAuthenticated } = useContext(AuthContext)

  const [listings, setListings] = useState<Listing[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [search, setSearch] = useState("")
  const [searchInput, setSearchInput] = useState("")
  const [category, setCategory] = useState("")

  const limit = 20
  const totalPages = Math.ceil(total / limit)

  useEffect(() => {
    setLoading(true)
    setError("")
    getListings({
      status: "active",
      page,
      limit,
      search: search || undefined,
      category: category || undefined,
    })
      .then((data) => {
        setListings(data.listings || [])
        setTotal(data.total || 0)
      })
      .catch(() => setError("Failed to load listings"))
      .finally(() => setLoading(false))
  }, [page, search, category])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    setSearch(searchInput)
  }

  const handleCategoryChange = (cat: string) => {
    setPage(1)
    setCategory(cat === "All" ? "" : cat)
  }

  return (
    <div className="app-screen">
      {/* Header */}
      <div className="app-header">
        <span className="app-header-title">YUTrade</span>
        <div style={{ display: "flex", gap: 8 }}>
          {isAuthenticated ? (
            <>
              <button className="app-header-btn" onClick={() => navigate("/create")} title="Create Listing">+</button>
              <button className="app-header-btn" onClick={() => navigate("/my-listings")} title="My Listings">👤</button>
              <button className="app-header-btn" onClick={() => { logout(); navigate("/login") }} title="Logout">⎋</button>
            </>
          ) : (
            <button className="btn-red" style={{ padding: "4px 12px", fontSize: 13 }} onClick={() => navigate("/login")}>
              Login
            </button>
          )}
        </div>
      </div>

      <div className="app-content">
        {/* Search bar */}
        <form onSubmit={handleSearch} style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <input
            className="auth-input"
            style={{ flex: 1, marginBottom: 0 }}
            type="text"
            placeholder="Search listings…"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button className="btn-red" type="submit" style={{ width: "auto", padding: "0 16px" }}>
            Search
          </button>
        </form>

        {/* Category filters */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
          {CATEGORIES.map((cat) => {
            const active = (cat === "All" && !category) || cat === category
            return (
              <button
                key={cat}
                onClick={() => handleCategoryChange(cat)}
                style={{
                  padding: "4px 12px",
                  borderRadius: 16,
                  border: "1px solid",
                  borderColor: active ? "#E31837" : "#ccc",
                  background: active ? "#E31837" : "#fff",
                  color: active ? "#fff" : "#333",
                  cursor: "pointer",
                  fontSize: 13,
                }}
              >
                {cat}
              </button>
            )
          })}
        </div>

        {/* Results */}
        {loading ? (
          <p style={{ textAlign: "center", paddingTop: 48, color: "#aaa" }}>Loading…</p>
        ) : error ? (
          <p style={{ textAlign: "center", paddingTop: 48, color: "#888" }}>{error}</p>
        ) : listings.length === 0 ? (
          <p style={{ textAlign: "center", paddingTop: 48, color: "#888" }}>No listings found.</p>
        ) : (
          <div className="listings-grid">
            {listings.map((listing) => {
              const firstImg = [...listing.images].sort((a, b) => a.position - b.position)[0]
              return (
                <div
                  key={listing.id}
                  className="listing-card"
                  onClick={() => navigate(`/listings/${listing.id}`)}
                  style={{ cursor: "pointer" }}
                >
                  <div className="listing-card-img">
                    {firstImg ? (
                      <img
                        src={`${API_URL}/${firstImg.file_path}`}
                        alt={listing.title}
                        style={{ width: "100%", height: "100%", objectFit: "cover" }}
                      />
                    ) : (
                      <span style={{ color: "#ccc", fontSize: 32 }}>🖼</span>
                    )}
                  </div>
                  <div className="listing-card-body">
                    <div className="listing-card-title">{listing.title}</div>
                    <div className="listing-card-price">${listing.price.toFixed(2)}</div>
                    {listing.category && (
                      <div className="listing-card-category">{listing.category}</div>
                    )}
                    <div className="listing-card-seller">{listing.seller.name}</div>
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div style={{ display: "flex", justifyContent: "center", gap: 8, marginTop: 24 }}>
            <button
              className="btn-outline"
              style={{ width: "auto", padding: "6px 16px" }}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              Previous
            </button>
            <span style={{ lineHeight: "36px", fontSize: 14, color: "#555" }}>
              {page} / {totalPages}
            </span>
            <button
              className="btn-outline"
              style={{ width: "auto", padding: "6px 16px" }}
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
