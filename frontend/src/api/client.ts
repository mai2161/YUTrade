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
import axios from "axios"
const apiclient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
    headers: {
        "Content-Type": "application/json",
    },
})
apiclient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token")
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)
apiclient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("access_token")
            window.location.href = "/login"
        }
        return Promise.reject(error)
    }
)
export default apiclient