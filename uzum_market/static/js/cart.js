// Load cart from localStorage
let cart = JSON.parse(localStorage.getItem("uzum_cart")) || []

// Render cart items
function renderCart() {
  const cartItemsContainer = document.getElementById("cart-items")
  const itemsCount = document.getElementById("items-count")
  const totalPrice = document.getElementById("total-price")

  if (cart.length === 0) {
    cartItemsContainer.innerHTML = `
            <div class="empty-message">
                <h3>Savat bo'sh</h3>
                <p>Mahsulotlar qo'shing</p>
                <a href="/api/products/home/" style="color: #7000FF; text-decoration: none; font-weight: 600;">
                    Xarid qilishni boshlash →
                </a>
            </div>
        `
    itemsCount.textContent = "0 ta"
    totalPrice.textContent = "0 so'm"
    return
  }

  let html = ""
  let total = 0
  let count = 0

  cart.forEach((item) => {
    const itemTotal = item.price * item.quantity
    total += itemTotal
    count += item.quantity

    html += `
            <div class="cart-item">
                <div class="cart-item-image">
                    <div class="image-placeholder">📷</div>
                </div>
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${item.price.toLocaleString()} so'm</div>
                    <div class="cart-item-controls">
                        <div class="quantity-control">
                            <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">−</button>
                            <span class="quantity-value">${item.quantity}</span>
                            <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                        </div>
                        <button class="btn-remove" onclick="removeFromCart(${item.id})">O'chirish</button>
                    </div>
                </div>
            </div>
        `
  })

  cartItemsContainer.innerHTML = html
  itemsCount.textContent = `${count} ta`
  totalPrice.textContent = `${total.toLocaleString()} so'm`
}

// Update quantity
function updateQuantity(productId, change) {
  const item = cart.find((i) => i.id === productId)
  if (item) {
    item.quantity += change
    if (item.quantity <= 0) {
      removeFromCart(productId)
    } else {
      localStorage.setItem("uzum_cart", JSON.stringify(cart))
      renderCart()
    }
  }
}

// Remove from cart
function removeFromCart(productId) {
  cart = cart.filter((item) => item.id !== productId)
  localStorage.setItem("uzum_cart", JSON.stringify(cart))
  renderCart()
}

// Place order
async function placeOrder() {
  const phone = document.getElementById("phone").value

  if (!phone) {
    alert("Telefon raqamingizni kiriting!")
    return
  }

  if (cart.length === 0) {
    alert("Savat bo'sh!")
    return
  }

  try {
    // Send orders to backend
    for (const item of cart) {
      const response = await fetch("/api/products/orders/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          product: item.id,
          quantity: item.quantity,
          phone_number: phone,
        }),
      })

      if (!response.ok) {
        throw new Error("Order failed")
      }
    }

    // Clear cart
    cart = []
    localStorage.setItem("uzum_cart", JSON.stringify(cart))

    alert("Buyurtma muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.")
    window.location.href = "/api/products/home/"
  } catch (error) {
    console.error("Error:", error)
    alert("Xatolik yuz berdi! Qaytadan urinib ko'ring.")
  }
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Initialize
document.addEventListener("DOMContentLoaded", renderCart)
