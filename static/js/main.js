// Product data
const products = [
    {
        id: 1,
        name: "Laptop Premium Pro",
        price: "Rp 15.999.000",
        image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"
    },
    {
        id: 2,
        name: "Smartphone X Pro",
        price: "Rp 12.499.000",
        image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80"
    },
    {
        id: 3,
        name: "Headphones Wireless",
        price: "Rp 2.999.000",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"
    },
    {
        id: 4,
        name: "Kamera Digital 4K",
        price: "Rp 8.999.000",
        image: "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=600&q=80"
    }
];

// Cart
let cart = [];

// Load products
function loadProducts() {
    const container = document.getElementById('products-container');
    // Cek jika container ada sebelum mengisinya
    if (container) {
        container.innerHTML = products.map(product => `
            <div class="product-card">
                <img src="${product.image}" alt="${product.name}" class="product-image">
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-price">${product.price}</p>
                    <button class="btn btn-primary" onclick="addToCart(${product.id})">Tambah ke Keranjang</button>
                </div>
            </div>
        `).join('');
    }
}

// Add to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    cart.push(product);
    updateCartCount();
    alert(`${product.name} ditambahkan ke keranjang!`);
}

// Update cart count
function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.length;
}

// Show cart
function showCart() {
    if (cart.length === 0) {
        alert('Keranjang belanja Anda kosong.');
    } else {
        const cartItems = cart.map(item => `- ${item.name} (${item.price})`).join('\n');
        alert(`Keranjang Belanja:\n\n${cartItems}\n\nTotal item: ${cart.length}`);
    }
}

// Subscribe newsletter
function subscribeNewsletter(event) {
    event.preventDefault();
    const email = event.target.querySelector('input[type="email"]').value;
    alert(`Terima kasih! Email ${email} telah terdaftar untuk newsletter kami.`);
    event.target.reset();
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Initialize
// Pastikan DOM sudah siap sebelum menjalankan fungsi
document.addEventListener('DOMContentLoaded', (event) => {
    loadProducts();
});