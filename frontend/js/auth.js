// ==========================================
// 1. LOGIN LOGIC
// ==========================================
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error-message");

    // FastAPI ko username aur password URL Encoded form mein chahiye hota hai
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Login failed. Check email and password.");
        }

        // Token save karein aur home page par bhej dein
        localStorage.setItem("access_token", data.access_token);
        alert("Login successful!");
        window.location.href = "index.html";

    } catch (error) {
        errorMsg.innerText = error.message;
        errorMsg.style.display = "block";
    }
});

// ==========================================
// 2. REGISTRATION LOGIC
// ==========================================
document.getElementById("register-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const name = document.getElementById("reg-name").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const errorMsg = document.getElementById("reg-error-message");

    try {
        // FastAPI mein naya user banane ka standard endpoint "/users/" hota hai. 
        // Agar aapke backend mein yeh "/auth/register" hai, toh yahan "/users/" ko change kar lein.
        const response = await apiRequest("/auth/register", {            method: "POST",
            body: JSON.stringify({ 
                full_name: name,
                email: email, 
                password: password 
            })
        });

        alert("Account created successfully! Please login now.");
        window.location.href = "login.html";
        
    } catch (error) {
        errorMsg.innerText = "Registration failed: " + error.message;
        errorMsg.style.display = "block";
    }
});