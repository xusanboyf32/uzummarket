// Cart management
const cart = JSON.parse(localStorage.getItem("uzum_cart")) || []
let wishlist = JSON.parse(localStorage.getItem("uzum_wishlist")) || []

// Update cart count
function updateCartCount() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0)
  const badge = document.getElementById("cart-count")
  if (badge) {
    badge.textContent = count
  }
}

// Update wishlist count
function updateWishlistCount() {
  const badge = document.getElementById("wishlist-count")
  if (badge) {
    badge.textContent = wishlist.length
  }
}

// Add to cart
function addToCart(productId, productName, price) {
  const existingItem = cart.find((item) => item.id === productId)

  if (existingItem) {
    existingItem.quantity += 1
  } else {
    cart.push({
      id: productId,
      name: productName,
      price: price,
      quantity: 1,
    })
  }

  localStorage.setItem("uzum_cart", JSON.stringify(cart))
  updateCartCount()

  // Show notification
  showNotification("Mahsulot savatga qo'shildi!")
}

// Toggle wishlist
async function toggleWishlist(productId) {
  try {
    const response = await fetch("/api/products/wishlist/toggle/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ product_id: productId }),
    })

    const data = await response.json()

    // Update UI
    const btn = document.querySelector(`[data-product-id="${productId}"] .wishlist-btn`)
    if (btn) {
      if (data.in_wishlist) {
        btn.classList.add("active")
        btn.querySelector(".heart").textContent = "❤️"
        showNotification("Sevimlilarga qo'shildi!")
      } else {
        btn.classList.remove("active")
        btn.querySelector(".heart").textContent = "🤍"
        showNotification("Sevimlilardan o'chirildi!")
      }
    }

    // Update wishlist in localStorage
    if (data.in_wishlist) {
      if (!wishlist.includes(productId)) {
        wishlist.push(productId)
      }
    } else {
      wishlist = wishlist.filter((id) => id !== productId)
    }
    localStorage.setItem("uzum_wishlist", JSON.stringify(wishlist))
    updateWishlistCount()
  } catch (error) {
    console.error("Error:", error)
    showNotification("Xatolik yuz berdi!", "error")
  }
}

// Show notification
function showNotification(message, type = "success") {
  const notification = document.createElement("div")
  notification.className = `notification ${type}`
  notification.textContent = message
  notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: ${type === "success" ? "#7000FF" : "#ff3333"};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `

  document.body.appendChild(notification)

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
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

// Load wishlist status on page load
async function loadWishlistStatus() {
  try {
    const response = await fetch("/api/products/wishlist/")
    const data = await response.json()

    wishlist = data.map((item) => item.product.id)
    localStorage.setItem("uzum_wishlist", JSON.stringify(wishlist))

    // Update UI
    wishlist.forEach((productId) => {
      const btn = document.querySelector(`[data-product-id="${productId}"] .wishlist-btn`)
      if (btn) {
        btn.classList.add("active")
        btn.querySelector(".heart").textContent = "❤️"
      }
    })

    updateWishlistCount()
  } catch (error) {
    console.error("Error loading wishlist:", error)
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  updateCartCount()
  updateWishlistCount()
  loadWishlistStatus()
})

// Add CSS animations
const style = document.createElement("style")
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`
document.head.appendChild(style)
