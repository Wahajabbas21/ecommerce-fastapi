// ==========================================
// 1. LOGIN LOGIC (Updated with RBAC Redirection)
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

        // 1. Token save karein
        localStorage.setItem("access_token", data.access_token);

        // 2. User ka role check karne ke liye profile fetch karein
        const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${data.access_token}`
            }
        });

        if (userResponse.ok) {
            const userData = await userResponse.json();
            
            // 3. Role-based redirection (Admin vs Normal User)
            if (userData.is_admin === true) {
                window.location.href = "admin/dashboard.html";
            } else {
                window.location.href = "index.html";
            }
        } else {
            // Agar profile fetch na ho sake toh default home par bhej dein
            window.location.href = "index.html";
        }

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
        // FastAPI mein naya user banane ka standard endpoint "/auth/register" ya "/users/" hai
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