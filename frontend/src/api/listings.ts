// Assigned to: Mai Komar
// Phase: 2 (F2.1)
//
// TODO: Listings API functions.
//
// import client from "./client"
// import { Listing, PaginatedListings } from "../types"
//
// getListings(params: { search?, category?, status?, page?, limit? }): Promise<PaginatedListings>
//   - GET /listings with query params
//   - Return response.data
//
// getListing(id: number): Promise<Listing>
//   - GET /listings/{id}
//   - Return response.data
//
// createListing(formData: FormData): Promise<Listing>
//   - POST /listings with FormData (multipart/form-data)
//   - Must set Content-Type header to "multipart/form-data"
//   - FormData should include: title, description, price, category, and images[] files
//   - Return response.data
//
// updateListing(id: number, data: { title?, description?, price?, status? }): Promise<Listing>
//   - PATCH /listings/{id} with JSON body
//   - Return response.data
