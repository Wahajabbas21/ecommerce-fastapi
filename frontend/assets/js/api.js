/**
 * API Helper Functions for making authenticated and unauthenticated requests
 */

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("access_token");
    
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        // Handle unauthorized or expired tokens
        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("API Request Error:", error);
        throw error;
    }
}