async function fetchCart() {
    const cartContainer = document.getElementById("cart-items");
    const cartTotalElement = document.getElementById("cart-total");

    if (!localStorage.getItem("access_token")) {
        cartContainer.innerHTML = "<p>Please <a href='login.html'>login</a> to view your cart.</p>";
        return;
    }

    try {
        const cart = await apiRequest("/cart/");
        const items = cart.items || [];

        if (!items || items.length === 0) {
            cartContainer.innerHTML = "<p>Your cart is empty.</p>";
            cartTotalElement.innerText = "Total: Rs. 0";
            return;
        }

        cartContainer.innerHTML = "";
        let calculatedTotal = 0;

        items.forEach(item => {
            const productName = item.product?.name || "Product";
            const productPrice = item.product?.price || 0;
            const quantity = item.quantity || 1;
            const itemTotal = productPrice * quantity;
            calculatedTotal += itemTotal;

            const itemDiv = document.createElement("div");
            itemDiv.className = "cart-item";
            itemDiv.style.display = "flex";
            itemDiv.style.justifyContent = "space-between";
            itemDiv.style.alignItems = "center";
            itemDiv.style.padding = "10px 0";
            itemDiv.style.borderBottom = "1px solid #e5e7eb";

            itemDiv.innerHTML = `
                <div>
                    <h4>${productName}</h4>
                    <p>Price: Rs. ${productPrice} x ${quantity} = <strong>Rs. ${itemTotal}</strong></p>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <button onclick="updateQuantity(${item.id}, ${quantity - 1})" style="padding: 4px 8px; cursor: pointer;">-</button>
                    <span>${quantity}</span>
                    <button onclick="updateQuantity(${item.id}, ${quantity + 1})" style="padding: 4px 8px; cursor: pointer;">+</button>
                    <button onclick="removeItem(${item.id})" style="background-color: #dc2626; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; margin-left: 10px;">Remove</button>
                </div>
            `;
            cartContainer.appendChild(itemDiv);
        });

        cartTotalElement.innerText = `Total: Rs. ${calculatedTotal}`;

    } catch (error) {
        cartContainer.innerHTML = `<p style="color: red;">Failed to load cart: ${error.message}</p>`;
    }
}

async function updateQuantity(itemId, newQuantity) {
    if (newQuantity <= 0) {
        removeItem(itemId);
        return;
    }
    try {
        await apiRequest(`/cart/items/${itemId}`, {
            method: "PUT",
            body: JSON.stringify({ quantity: newQuantity })
        });
        fetchCart();
    } catch (error) {
        alert("Failed to update quantity: " + error.message);
    }
}

async function removeItem(itemId) {
    try {
        await apiRequest(`/cart/items/${itemId}`, {
            method: "DELETE"
        });
        fetchCart();
    } catch (error) {
        alert("Failed to remove item: " + error.message);
    }
}

fetchCart();