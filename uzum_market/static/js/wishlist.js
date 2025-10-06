// Load wishlist
async function loadWishlist() {
  try {
    const response = await fetch("/api/products/wishlist/")
    const data = await response.json()

    const container = document.getElementById("wishlist-products")

    if (data.length === 0) {
      container.innerHTML = `
                <div class="empty-message" style="grid-column: 1/-1;">
                    <h3>Sevimlilar bo'sh</h3>
                    <p>Mahsulotlarni sevimlilar ro'yxatiga qo'shing</p>
                    <a href="/api/products/home/" style="color: #7000FF; text-decoration: none; font-weight: 600;">
                        Xarid qilishni boshlash →
                    </a>
                </div>
            `
      return
    }

    let html = ""
    data.forEach((item) => {
      const product = item.product
      const price = product.discount_price || product.price

      html += `
                <div class="product-card" data-product-id="${product.id}">
                    <button class="wishlist-btn active" onclick="removeFromWishlist(${product.id})">
                        <span class="heart">❤️</span>
                    </button>
                    <div class="product-image">
                        ${
                          product.images && product.images.length > 0
                            ? `<img src="${product.images[0].image}" alt="${product.name}">`
                            : '<div class="image-placeholder">📷</div>'
                        }
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">${product.name}</h3>
                        <p class="product-description">${product.short_description || ""}</p>
                        <div class="product-price">
                            ${
                              product.discount_price
                                ? `<span class="price-old">${product.price} so'm</span>
                                   <span class="price-new">${product.discount_price} so'm</span>`
                                : `<span class="price-current">${product.price} so'm</span>`
                            }
                        </div>
                        <button class="btn-add-cart" onclick="addToCartFromWishlist(${product.id}, '${product.name}', ${price})">
                            Savatga qo'shish
                        </button>
                    </div>
                </div>
            `
    })

    container.innerHTML = html
  } catch (error) {
    console.error("Error loading wishlist:", error)
  }
}

// Remove from wishlist
async function removeFromWishlist(productId) {
  try {
    const response = await fetch("/api/products/wishlist/toggle/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ product_id: productId }),
    })

    if (response.ok) {
      loadWishlist()
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

// Add to cart from wishlist
function addToCartFromWishlist(productId, productName, price) {
  const cart = JSON.parse(localStorage.getItem("uzum_cart")) || []

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
  alert("Mahsulot savatga qo'shildi!")
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
document.addEventListener("DOMContentLoaded", loadWishlist)
