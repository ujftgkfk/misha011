// Products Database
const products = [
    {
        id: 1,
        name: 'iPhone 15 Pro',
        category: 'smartphones',
        price: 89990,
        description: 'Новейший флагманский смартфон Apple с чипом A17 Pro',
        icon: '📱'
    },
    {
        id: 2,
        name: 'Samsung Galaxy S24',
        category: 'smartphones',
        price: 74990,
        description: 'Мощный Android-смартфон с AI-функциями',
        icon: '📱'
    },
    {
        id: 3,
        name: 'MacBook Pro 16"',
        category: 'laptops',
        price: 249990,
        description: 'Профессиональный ноутбук с чипом M3 Pro',
        icon: '💻'
    },
    {
        id: 4,
        name: 'Dell XPS 15',
        category: 'laptops',
        price: 149990,
        description: 'Премиальный Windows ноутбук для работы и творчества',
        icon: '💻'
    },
    {
        id: 5,
        name: 'AirPods Pro 2',
        category: 'audio',
        price: 22990,
        description: 'Беспроводные наушники с активным шумоподавлением',
        icon: '🎧'
    },
    {
        id: 6,
        name: 'Sony WH-1000XM5',
        category: 'audio',
        price: 29990,
        description: 'Топовые накладные наушники с лучшим шумоподавлением',
        icon: '🎧'
    },
    {
        id: 7,
        name: 'iPad Air',
        category: 'accessories',
        price: 64990,
        description: 'Универсальный планшет для работы и развлечений',
        icon: '📱'
    },
    {
        id: 8,
        name: 'Apple Watch Series 9',
        category: 'accessories',
        price: 39990,
        description: 'Умные часы с расширенными функциями здоровья',
        icon: '⌚'
    },
    {
        id: 9,
        name: 'Magic Keyboard',
        category: 'accessories',
        price: 9990,
        description: 'Беспроводная клавиатура Apple с отличной эргономикой',
        icon: '⌨️'
    },
    {
        id: 10,
        name: 'Logitech MX Master 3S',
        category: 'accessories',
        price: 8990,
        description: 'Профессиональная беспроводная мышь для продуктивности',
        icon: '🖱️'
    },
    {
        id: 11,
        name: 'Samsung 27" 4K',
        category: 'accessories',
        price: 34990,
        description: 'Монитор 4K с HDR для работы и игр',
        icon: '🖥️'
    },
    {
        id: 12,
        name: 'JBL Charge 5',
        category: 'audio',
        price: 12990,
        description: 'Портативная Bluetooth колонка с мощным звуком',
        icon: '🔊'
    }
];

// Format price in rubles
function formatPrice(price) {
    return price.toLocaleString('ru-RU') + ' ₽';
}

// Create product card HTML
function createProductCard(product) {
    return `
        <div class="product-card">
            <div class="product-image">${product.icon}</div>
            <div class="product-info">
                <div class="product-category">${getCategoryName(product.category)}</div>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <span class="product-price">${formatPrice(product.price)}</span>
                    <button class="btn-add-cart" onclick="addToCart(${product.id})">
                        В корзину
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Get category display name
function getCategoryName(category) {
    const categories = {
        'smartphones': 'Смартфоны',
        'laptops': 'Ноутбуки',
        'accessories': 'Аксессуары',
        'audio': 'Аудио'
    };
    return categories[category] || category;
}

// Load featured products on home page
function loadFeaturedProducts() {
    const container = document.getElementById('featured-products');
    if (!container) return;

    // Show first 4 products
    const featured = products.slice(0, 4);
    container.innerHTML = featured.map(createProductCard).join('');
}

// Load all products on products page
function loadAllProducts() {
    const container = document.getElementById('all-products');
    if (!container) return;

    displayProducts(products);
}

// Display filtered/sorted products
function displayProducts(productsToDisplay) {
    const container = document.getElementById('all-products');
    if (!container) return;

    if (productsToDisplay.length === 0) {
        container.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">Товары не найдены</p>';
        return;
    }

    container.innerHTML = productsToDisplay.map(createProductCard).join('');
}

// Filter products by category
function filterProducts() {
    const categoryFilter = document.getElementById('category-filter');
    const sortFilter = document.getElementById('sort-filter');

    if (!categoryFilter || !sortFilter) return;

    let filtered = [...products];

    // Apply category filter
    const category = categoryFilter.value;
    if (category !== 'all') {
        filtered = filtered.filter(p => p.category === category);
    }

    // Apply sorting
    const sort = sortFilter.value;
    switch (sort) {
        case 'price-low':
            filtered.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filtered.sort((a, b) => b.price - a.price);
            break;
        case 'name':
            filtered.sort((a, b) => a.name.localeCompare(b.name, 'ru'));
            break;
    }

    displayProducts(filtered);
}

// Setup filter listeners
function setupFilters() {
    const categoryFilter = document.getElementById('category-filter');
    const sortFilter = document.getElementById('sort-filter');

    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }
    if (sortFilter) {
        sortFilter.addEventListener('change', filterProducts);
    }
}

// Get product by ID
function getProductById(id) {
    return products.find(p => p.id === id);
}

// Initialize products on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedProducts();
    loadAllProducts();
    setupFilters();
});
