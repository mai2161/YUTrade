// Assigned to: Mai Komar
// Phase: 1 (F1.8)
//
// TODO: Auth API functions.
//
// import client from "./client"
// import { RegisterRequest, LoginRequest, VerifyRequest, TokenResponse } from "../types"
//
// register(data: RegisterRequest): Promise
//   - POST /auth/register with { email, password, name }
//   - Return response.data
//
// verify(data: VerifyRequest): Promise
//   - POST /auth/verify with { email, code }
//   - Return response.data
//
// login(data: LoginRequest): Promise<TokenResponse>
//   - POST /auth/login with { email, password }
//   - Return response.data (contains access_token, token_type, user)

import client from "./client"
import { RegisterRequest, LoginRequest, VerifyRequest} from "../types"

export const register = (data: RegisterRequest) => {
    return client.post("/auth/register", data).then((response) => response.data)
}

export const verify = (data: VerifyRequest) => {
    return client.post("/auth/verify", data).then((response) => response.data)
}

export const login = (data: LoginRequest) => {
    return client.post("/auth/login", data).then((response) => response.data)
}

export const resendVerification = (email: string) => {
    return client.post(`/auth/resend-verification?email=${encodeURIComponent(email)}`).then((response) => response.data)
}
