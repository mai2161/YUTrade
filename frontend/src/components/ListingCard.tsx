// Assigned to: Harnaindeep Kaur
// Phase: 2 (F2.2)
//
// TODO: Card component for displaying a listing in the browse grid.
//
// Props:
//   - listing: Listing (from types/index.ts)
//
// Structure:
//   <div className="listing-card" onClick={() => navigate(`/listings/${listing.id}`)}>
//     <div className="listing-card-image">
//       {listing.images.length > 0
//         ? <img src={`${API_URL}/${listing.images[0].file_path}`} alt={listing.title} />
//         : <div className="no-image-placeholder">No Image</div>
//       }
//     </div>
//     <div className="listing-card-body">
//       <h3 className="listing-card-title">{listing.title}</h3>
//       <p className="listing-card-price">${listing.price.toFixed(2)}</p>
//       {listing.category && <span className="listing-card-category">{listing.category}</span>}
//       <p className="listing-card-date">{formatted date}</p>
//     </div>
//   </div>
//
// Styling:
//   - Card with border/shadow, rounded corners
//   - Image takes top portion, fixed aspect ratio
//   - Price in bold, possibly YU red color
//   - Category as a small badge/tag
//   - Hover effect (slight shadow increase or scale)
