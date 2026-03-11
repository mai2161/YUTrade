// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.3)
//
// TODO: Define all TypeScript interfaces used across the frontend.
//
// User:
//   id: number
//   email: string
//   name: string
//   is_verified: boolean
//   created_at: string  (ISO datetime string)
//
// TokenResponse:
//   access_token: string
//   token_type: string
//   user: User
//
// Listing:
//   id: number
//   seller_id: number
//   seller: { id: number; name: string; email: string }
//   title: string
//   description: string | null
//   price: number
//   category: string | null
//   status: "active" | "sold" | "removed"
//   images: Image[]
//   created_at: string
//   updated_at: string
//
// Image:
//   id: number
//   file_path: string
//   position: number
//
// PaginatedListings:
//   listings: Listing[]
//   total: number
//   page: number
//   limit: number
//
// Message:
//   id: number
//   listing_id: number
//   sender_id: number
//   receiver_id: number
//   sender: { id: number; name: string }
//   content: string
//   created_at: string
//
// RegisterRequest:
//   email: string
//   password: string
//   name: string
//
// LoginRequest:
//   email: string
//   password: string
//
// VerifyRequest:
//   email: string
//   code: string
//
// ListingCreateForm:
//   title: string
//   description: string
//   price: number
//   category: string
//   images: File[]
//
// MessageCreateRequest:
//   content: string

export interface User {
    id: number
    email: string
    name: string
    is_verified: boolean
    created_at: string
}
export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Image {
  id: number;
  file_path: string;
  position: number;
}

export interface Listing {
  id: number;
  seller_id: number;
  seller: { id: number; name: string; email: string };
  title: string;
  description: string | null;
  price: number;
  category: string | null;
  status: "active" | "sold" | "removed";
  images: Image[];
  created_at: string;
  updated_at: string;
}

export interface PaginatedListings {
  listings: Listing[];
  total: number;
  page: number;
  limit: number;
}

export interface Message {
  id: number;
  listing_id: number;
  sender_id: number;
  receiver_id: number;
  sender: { id: number; name: string };
  content: string;
  created_at: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface VerifyRequest {
  email: string;
  code: string;
}

export interface ListingCreateForm {
  title: string;
  description: string;
  price: number;
  category: string;
  images: File[];
}

export interface MessageCreateRequest {
  content: string;
}
