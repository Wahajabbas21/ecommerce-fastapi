// Base URL for our FastAPI backend
const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

/**
 * Reusable function to make API requests
 * @param {string} endpoint - The API endpoint (e.g., "/products")
 * @param {object} options - Fetch options (method, body, etc.)
 */
async function apiRequest(endpoint, options = {}) {
    // Get token from localStorage if user is logged in
    const token = localStorage.getItem("access_token");
    
    // Set default headers
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    // Add Authorization header if token exists
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        // Parse JSON response
        const data = await response.json().catch(() => null);

        // Handle HTTP errors
        if (!response.ok) {
            const errorMessage = data?.detail || "An error occurred";
            throw new Error(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        }

        return data;
    } catch (error) {
        console.error("API Request Error:", error);
        throw error;
    }
}