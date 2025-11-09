// Данные товаров
const products = [
    {
        id: 1,
        name: "Смартфон Samsung Galaxy",
        category: "electronics",
        price: 45000,
        description: "Современный смартфон с отличной камерой",
        icon: "📱"
    },
    {
        id: 2,
        name: "Ноутбук ASUS",
        category: "electronics",
        price: 65000,
        description: "Мощный ноутбук для работы и игр",
        icon: "💻"
    },
    {
        id: 3,
        name: "Беспроводные наушники",
        category: "electronics",
        price: 8500,
        description: "Наушники с шумоподавлением",
        icon: "🎧"
    },
    {
        id: 4,
        name: "Футболка Premium",
        category: "clothing",
        price: 1500,
        description: "Качественная хлопковая футболка",
        icon: "👕"
    },
    {
        id: 5,
        name: "Джинсы классические",
        category: "clothing",
        price: 3500,
        description: "Стильные джинсы прямого кроя",
        icon: "👖"
    },
    {
        id: 6,
        name: "Кроссовки спортивные",
        category: "clothing",
        price: 5500,
        description: "Удобные кроссовки для спорта",
        icon: "👟"
    },
    {
        id: 7,
        name: "Программирование на JavaScript",
        category: "books",
        price: 1200,
        description: "Учебник для начинающих разработчиков",
        icon: "📚"
    },
    {
        id: 8,
        name: "Искусство войны",
        category: "books",
        price: 800,
        description: "Классическая книга по стратегии",
        icon: "📖"
    },
    {
        id: 9,
        name: "Кофеварка автоматическая",
        category: "home",
        price: 12000,
        description: "Кофеварка с автоматическим помолом",
        icon: "☕"
    },
    {
        id: 10,
        name: "Настольная лампа LED",
        category: "home",
        price: 2500,
        description: "Современная LED лампа для рабочего стола",
        icon: "💡"
    },
    {
        id: 11,
        name: "Пылесос робот",
        category: "home",
        price: 18000,
        description: "Умный робот-пылесос с навигацией",
        icon: "🤖"
    },
    {
        id: 12,
        name: "Планшет iPad",
        category: "electronics",
        price: 55000,
        description: "Планшет для работы и развлечений",
        icon: "📲"
    }
];

// Состояние приложения
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let filteredProducts = [...products];

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    displayProducts(products);
    updateCartUI();
});

// Отображение товаров
function displayProducts(productsToDisplay) {
    const productsGrid = document.getElementById('products-grid');

    if (productsToDisplay.length === 0) {
        productsGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #999;"><h2>Товары не найдены</h2><p>Попробуйте изменить параметры поиска</p></div>';
        return;
    }

    productsGrid.innerHTML = productsToDisplay.map(product => `
        <div class="product-card">
            <div class="product-image">${product.icon}</div>
            <div class="product-info">
                <div class="product-category">${getCategoryName(product.category)}</div>
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description}</div>
                <div class="product-footer">
                    <div class="product-price">${formatPrice(product.price)}</div>
                    <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                        В корзину
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Получить название категории на русском
function getCategoryName(category) {
    const categories = {
        'electronics': 'Электроника',
        'clothing': 'Одежда',
        'books': 'Книги',
        'home': 'Для дома'
    };
    return categories[category] || category;
}

// Форматирование цены
function formatPrice(price) {
    return price.toLocaleString('ru-RU') + ' ₽';
}

// Фильтрация товаров
function filterProducts() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const minPrice = parseFloat(document.getElementById('min-price').value) || 0;
    const maxPrice = parseFloat(document.getElementById('max-price').value) || Infinity;

    // Получаем выбранные категории
    const categoryCheckboxes = document.querySelectorAll('input[name="category"]:checked');
    const selectedCategories = Array.from(categoryCheckboxes).map(cb => cb.value);

    // Если выбрана категория "all", показываем все товары
    const showAll = selectedCategories.includes('all');

    filteredProducts = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) ||
                            product.description.toLowerCase().includes(searchTerm);
        const matchesPrice = product.price >= minPrice && product.price <= maxPrice;
        const matchesCategory = showAll || selectedCategories.length === 0 ||
                               selectedCategories.includes(product.category);

        return matchesSearch && matchesPrice && matchesCategory;
    });

    displayProducts(filteredProducts);
}

// Сортировка товаров
function sortProducts() {
    const sortValue = document.getElementById('sort-select').value;

    switch(sortValue) {
        case 'price-asc':
            filteredProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-desc':
            filteredProducts.sort((a, b) => b.price - a.price);
            break;
        case 'name-asc':
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name, 'ru'));
            break;
        case 'name-desc':
            filteredProducts.sort((a, b) => b.name.localeCompare(a.name, 'ru'));
            break;
        default:
            filteredProducts = [...products];
    }

    displayProducts(filteredProducts);
}

// Добавление товара в корзину
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }

    saveCart();
    updateCartUI();
    showNotification(`${product.name} добавлен в корзину`);
}

// Удаление товара из корзины
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
    displayCart();
}

// Изменение количества товара
function changeQuantity(productId, delta) {
    const item = cart.find(item => item.id === productId);

    if (item) {
        item.quantity += delta;

        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartUI();
            displayCart();
        }
    }
}

// Очистка корзины
function clearCart() {
    if (cart.length === 0) return;

    if (confirm('Вы уверены, что хотите очистить корзину?')) {
        cart = [];
        saveCart();
        updateCartUI();
        displayCart();
        showNotification('Корзина очищена');
    }
}

// Сохранение корзины в localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Обновление UI корзины
function updateCartUI() {
    const cartCount = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

// Отображение содержимого корзины
function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart">Корзина пуста</div>';
        cartTotal.textContent = '0 ₽';
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.icon} ${item.name}</div>
                <div class="cart-item-price">${formatPrice(item.price)} × ${item.quantity}</div>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="changeQuantity(${item.id}, -1)">-</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="quantity-btn" onclick="changeQuantity(${item.id}, 1)">+</button>
                </div>
                <button class="remove-btn" onclick="removeFromCart(${item.id})">Удалить</button>
            </div>
        </div>
    `).join('');

    cartTotal.textContent = formatPrice(total);
}

// Переключение видимости корзины
function toggleCart() {
    const cartModal = document.getElementById('cart-modal');
    cartModal.classList.toggle('active');

    if (cartModal.classList.contains('active')) {
        displayCart();
    }
}

// Оформление заказа
function checkout() {
    if (cart.length === 0) {
        alert('Корзина пуста!');
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);

    alert(`Заказ оформлен!\n\nТоваров: ${itemCount}\nСумма: ${formatPrice(total)}\n\nСпасибо за покупку!`);

    cart = [];
    saveCart();
    updateCartUI();
    toggleCart();
}

// Показ уведомления
function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 2000);
}

// Закрытие корзины по клику вне её
document.getElementById('cart-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        toggleCart();
    }
});
