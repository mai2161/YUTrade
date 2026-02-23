// Assigned to: Harnaindeep Kaur
// Phase: 3 (F3.5)
//
// TODO: Search and filter bar for the BrowsePage.
//
// Props:
//   - onSearch(params: { search?, category?, min_price?, max_price? }): void
//       Callback to trigger a new search in BrowsePage
//
// Structure:
//   <div className="search-bar">
//     <input type="text" placeholder="Search listings..." value={search} onChange={...} />
//     <select value={category} onChange={...}>
//       <option value="">All Categories</option>
//       <option value="Textbooks">Textbooks</option>
//       <option value="Electronics">Electronics</option>
//       <option value="Furniture">Furniture</option>
//       <option value="Clothing">Clothing</option>
//       <option value="Other">Other</option>
//     </select>
//     <input type="number" placeholder="Min Price" value={minPrice} onChange={...} />
//     <input type="number" placeholder="Max Price" value={maxPrice} onChange={...} />
//     <button onClick={handleSearch}>Search</button>
//   </div>
//
// Behavior:
//   1. Maintain local state for search, category, minPrice, maxPrice
//   2. On "Search" click (or Enter key), call onSearch with current filter values
//   3. Omit empty/null values from the params object
//   4. Optional: debounce text input for live search
//
// Styling: Horizontal bar, inputs side by side, responsive (stack on mobile)
