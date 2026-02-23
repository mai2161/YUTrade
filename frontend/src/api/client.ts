// Assigned to: Mai Komar
// Phase: 1 (F1.2)
//
// TODO: Create Axios instance with JWT interceptor.
//
// 1. Import axios from "axios"
// 2. Create an axios instance with:
//    - baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000"
//    - headers: { "Content-Type": "application/json" }
//
// 3. Add a request interceptor:
//    - Read token from localStorage.getItem("access_token")
//    - If token exists, set config.headers.Authorization = `Bearer ${token}`
//    - Return config
//
// 4. Add a response interceptor:
//    - On 401 error: clear localStorage token, redirect to /login
//    - Return Promise.reject(error) for other errors
//
// 5. Export the axios instance as default
