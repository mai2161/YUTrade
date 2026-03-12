// Assigned to: Harnaindeep Kaur
// Phase: 2 (F2.6)

import React, { useState, useEffect, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { getListings, updateListing } from "../api/listings"
import { Listing } from "../types"
import { AuthContext } from "../context/AuthContext"

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

function statusLabel(status: string) {
  if (status === "active") return "Active"
  if (status === "sold") return "Sold"
  return "Inactive"
}

function statusClass(status: string) {
  if (status === "active") return "status-pill status-pill-active"
  if (status === "sold") return "status-pill status-pill-sold"
  return "status-pill status-pill-inactive"
}

export default function MyListingsPage() {
  const { user } = useContext(AuthContext)
  const navigate = useNavigate()
  const [listings, setListings] = useState<Listing[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getListings({})
      .then((data) => {
        const all: Listing[] = data.listings || []
        setListings(all.filter((l) => l.seller_id === user?.id))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [user])

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this listing?")) return
    try {
      await updateListing(id, { status: "removed" })
      setListings((prev) => prev.filter((l) => l.id !== id))
    } catch {
      alert("Failed to delete listing.")
    }
  }

  return (
    <div className="app-screen">
      <div className="app-header">
        <button className="app-header-btn" onClick={() => navigate(-1)}>
          ←
        </button>
        <span className="app-header-title">My Listings</span>
        <button className="app-header-btn" onClick={() => navigate("/my-listings")}>
          👤
        </button>
      </div>

      <div className="app-content">
        {loading ? (
          <p style={{ textAlign: "center", paddingTop: 48, color: "#aaa" }}>Loading…</p>
        ) : listings.length === 0 ? (
          <div style={{ textAlign: "center", paddingTop: 48 }}>
            <p style={{ color: "#888", marginBottom: 16 }}>
              You haven't created any listings yet.
            </p>
            <button className="btn-red" style={{ width: "auto", padding: "8px 20px" }} onClick={() => navigate("/create")}>
              Create Listing
            </button>
          </div>
        ) : (
          <div className="listings-table-wrap">
            <table className="listings-table">
              <thead>
                <tr>
                  <th></th>
                  <th>Title</th>
                  <th>Price</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th></th>
                </tr>
              </thead>
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
                      <td
                        style={{ maxWidth: 88, wordBreak: "break-word", cursor: "pointer" }}
                        onClick={() => navigate(`/listings/${listing.id}`)}
                      >
                        {listing.title}
                      </td>
                      <td>${listing.price.toFixed(2)}</td>
                      <td>{listing.category || "—"}</td>
                      <td>
                        <span className={statusClass(listing.status)}>
                          {statusLabel(listing.status)}
                        </span>
                      </td>
                      <td style={{ whiteSpace: "nowrap" }}>
                        <button
                          className="btn-table-action"
                          onClick={() => navigate(`/listings/${listing.id}/edit`)}
                        >
                          Edit Listing
                        </button>
                        <button
                          className="btn-table-action"
                          onClick={() => handleDelete(listing.id)}
                        >
                          Delete Listing
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
