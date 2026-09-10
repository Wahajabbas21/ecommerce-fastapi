async function fetchAndRenderProducts() {
    const container = document.getElementById("products-container");
    const loadingState = document.getElementById("loading-state");

    try {
        const products = await apiRequest("/products");
        loadingState.style.display = "none";

        if (!products || products.length === 0) {
            container.innerHTML = "<p>No products found in the database.</p>";
            return;
        }

        products.forEach(product => {
            const card = document.createElement("div");
            card.className = "product-card";
            card.innerHTML = `
                <h3>${product.name}</h3>
                <p>${product.description || "No description available"}</p>
                <p class="price">Rs. ${product.price}</p>
                <p><small>Stock: ${product.stock > 0 ? product.stock : "Out of stock"}</small></p>
                <button onclick="addToCart(${product.id})" ${product.stock === 0 ? "disabled" : ""}>
                    Add to Cart
                </button>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        loadingState.innerText = "Failed to load products.";
        console.error("Error:", error);
    }
}

// Add to Cart Function
async function addToCart(productId) {
    if (!localStorage.getItem("access_token")) {
        alert("Please login first to add items to your cart!");
        window.location.href = "login.html";
        return;
    }

    try {
        await apiRequest("/cart/", {
            method: "POST",
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });
        
        alert("Product added to cart successfully!");
    } catch (error) {
        alert("Error adding to cart: " + error.message);
    }
}

// Fetch products when page loads
fetchAndRenderProducts();