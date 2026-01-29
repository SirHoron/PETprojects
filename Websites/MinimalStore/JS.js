// Данные товаров
const products = [
    {
        id: 1,
        name: "Минималистичные наушники",
        category: "electronics",
        price: 12990,
        oldPrice: 15990,
        description: "Беспроводные наушники с чистым звуком и элегантным дизайном. До 24 часов работы.",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: "Хит"
    },
    {
        id: 2,
        name: "Стул Eames",
        category: "furniture",
        price: 45990,
        oldPrice: null,
        description: "Классический стул в минималистичном стиле. Комфорт и эстетика в каждой детали.",
        image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: null
    },
    {
        id: 3,
        name: "Умные часы",
        category: "electronics",
        price: 32990,
        oldPrice: 39990,
        description: "Тонкие умные часы с мониторингом здоровья и уведомлениями. Стиль и функциональность.",
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: "Скидка"
    },
    {
        id: 4,
        name: "Настольная лампа",
        category: "furniture",
        price: 8990,
        oldPrice: 11990,
        description: "Современная настольная лампа с регулируемой яркостью и температурой света.",
        image: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: null
    },
    {
        id: 5,
        name: "Минималистичный кошелек",
        category: "accessories",
        price: 4990,
        oldPrice: null,
        description: "Тонкий кошелек из натуральной кожи. Вмещает все необходимое без лишнего объема.",
        image: "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: "Новинка"
    },
    {
        id: 6,
        name: "Беспроводная клавиатура",
        category: "electronics",
        price: 7590,
        oldPrice: 9990,
        description: "Ультратонкая беспроводная клавиатура с подсветкой и длительным временем работы.",
        image: "https://images.unsplash.com/photo-1541140532154-b024d705b90a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: null
    },
    {
        id: 7,
        name: "Журнальный столик",
        category: "furniture",
        price: 24990,
        oldPrice: 29990,
        description: "Минималистичный стеклянный столик на деревянной основе. Идеально для современного интерьера.",
        image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: "Скидка"
    },
    {
        id: 8,
        name: "Минималистичные часы",
        category: "accessories",
        price: 12990,
        oldPrice: null,
        description: "Наручные часы с чистым циферблатом и кожаным ремешком. Вечная классика.",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        badge: null
    }
];
// Корзина
let cart = JSON.parse(localStorage.getItem('minimalstore_cart')) || [];
let currentCheckoutStep = 1;
let orderData = {};
// DOM элементы
const pages = document.querySelectorAll('.page');
const navLinks = document.querySelectorAll('[data-page]');
const cartCount = document.getElementById('cart-count');
const cartItemsContainer = document.getElementById('cart-items');
const emptyCart = document.getElementById('empty-cart');
const cartSummary = document.getElementById('cart-summary');
const productsGrid = document.getElementById('products-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const searchInput = document.getElementById('search-input');
const addToCartAnimation = document.getElementById('add-to-cart-animation');
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinksContainer = document.querySelector('.nav-links');
// Элементы оформления заказа
const checkoutSteps = document.querySelectorAll('.step');
const checkoutForms = {
    info: document.getElementById('checkout-form-info'),
    shipping: document.getElementById('checkout-form-shipping'),
    payment: document.getElementById('checkout-form-payment'),
    confirm: document.getElementById('checkout-form-confirm')
};
// Инициализация приложения
function init() {
    renderProducts();
    updateCartDisplay();
    setupEventListeners();
    
    // Показать страницу из hash, если есть
    const hash = window.location.hash.substring(1);
    if (hash && document.getElementById(hash)) {
        navigateToPage(hash);
    }
}
// Рендер товаров
function renderProducts(filter = 'all', search = '') {
    productsGrid.innerHTML = '';
    
    let filteredProducts = products;
    
    // Применение фильтра по категории
    if (filter !== 'all') {
        filteredProducts = filteredProducts.filter(product => product.category === filter);
    }
    
    // Применение поиска
    if (search) {
        const searchLower = search.toLowerCase();
        filteredProducts = filteredProducts.filter(product => 
            product.name.toLowerCase().includes(searchLower) || 
            product.description.toLowerCase().includes(searchLower)
        );
    }
    
    // Анимация появления товаров с задержкой
    filteredProducts.forEach((product, index) => {
        const productElement = createProductElement(product);
        productElement.style.animationDelay = `${index * 0.1}s`;
        productsGrid.appendChild(productElement);
    });
}
// Создание элемента товара
function createProductElement(product) {
    const div = document.createElement('div');
    div.className = 'product-card';
    
    // Проверяем, есть ли товар в корзине
    const inCart = cart.find(item => item.id === product.id);
    
    div.innerHTML = `
        <div class="product-image">
            ${product.badge ? `<div class="product-badge">${product.badge}</div>` : ''}
            <img src="${product.image}" alt="${product.name}">
        </div>
        <div class="product-info">
            <div class="product-category">${getCategoryName(product.category)}</div>
            <h3 class="product-name">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-footer">
                <div class="product-price">
                    ${product.oldPrice ? `<span class="old-price">${formatPrice(product.oldPrice)}</span>` : ''}
                    <span>${formatPrice(product.price)}</span>
                </div>
                <button class="add-to-cart-btn ${inCart ? 'added' : ''}" data-id="${product.id}">
                    <i class="fas ${inCart ? 'fa-check' : 'fa-plus'}"></i>
                </button>
            </div>
        </div>
    `;
    
    return div;
}
// Обновление отображения корзины
function updateCartDisplay() {
    // Обновление счетчика в шапке
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Сохранение в localStorage
    localStorage.setItem('minimalstore_cart', JSON.stringify(cart));
    
    // Обновление страницы корзины, если она активна
    if (document.getElementById('cart').classList.contains('active')) {
        renderCartItems();
        updateCartSummary();
    }
}
// Рендер товаров в корзине
function renderCartItems() {
    cartItemsContainer.innerHTML = '';
    
    if (cart.length === 0) {
        emptyCart.style.display = 'block';
        cartSummary.style.display = 'none';
        return;
    }
    
    emptyCart.style.display = 'none';
    cartSummary.style.display = 'block';
    
    cart.forEach(item => {
        const product = products.find(p => p.id === item.id);
        if (!product) return;
        
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-image">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="cart-item-info">
                <h4 class="cart-item-name">${product.name}</h4>
                <div class="cart-item-category">${getCategoryName(product.category)}</div>
                <div class="cart-item-price">${formatPrice(product.price)}</div>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-controls">
                    <button class="quantity-btn decrease-quantity" data-id="${product.id}">
                        <i class="fas fa-minus"></i>
                    </button>
                    <span class="quantity-value">${item.quantity}</span>
                    <button class="quantity-btn increase-quantity" data-id="${product.id}">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <button class="remove-item-btn" data-id="${product.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        cartItemsContainer.appendChild(cartItem);
    });
}
// Обновление итогов корзины
function updateCartSummary() {
    const subtotal = cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.id);
        return sum + (product.price * item.quantity);
    }, 0);
    
    // Рассчет стоимости доставки
    let shipping = 0;
    if (subtotal > 0 && subtotal < 10000) {
        shipping = 300;
    } else if (subtotal === 0) {
        shipping = 0;
    }
    
    const total = subtotal + shipping;
    
    document.getElementById('subtotal').textContent = `${formatPrice(subtotal)}`;
    document.getElementById('shipping').textContent = `${formatPrice(shipping)}`;
    document.getElementById('total').textContent = `${formatPrice(total)}`;
    
    // Обновление количества товаров в итогах
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelector('.summary-row span:first-child').textContent = `Товары (${totalItems})`;
}
// Навигация между страницами
function navigateToPage(pageId) {
    // Скрыть все страницы
    pages.forEach(page => {
        page.classList.remove('active');
    });
    
    // Показать выбранную страницу
    document.getElementById(pageId).classList.add('active');
    
    // Обновить URL hash
    window.location.hash = pageId;
    
    // Обновить навигацию
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageId) {
            link.classList.add('active');
        }
    });
    
    // Обновить данные на странице, если нужно
    if (pageId === 'cart') {
        renderCartItems();
        updateCartSummary();
    } else if (pageId === 'home') {
        // Сбросить фильтры к активному
        const activeFilter = document.querySelector('.filter-btn.active');
        if (activeFilter) {
            renderProducts(activeFilter.dataset.filter, searchInput.value);
        }
    }
    
    // Закрыть мобильное меню
    if (window.innerWidth <= 768) {
        navLinksContainer.classList.remove('active');
    }
}
// Добавление товара в корзину с анимацией
function addToCart(productId, button) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    // Находим кнопку, если не передана
    if (!button) {
        button = document.querySelector(`.add-to-cart-btn[data-id="${productId}"]`);
    }
    
    // Анимация кнопки
    button.classList.add('added');
    button.innerHTML = '<i class="fas fa-check"></i>';
    
    // Через 1 секунду возвращаем обычное состояние
    setTimeout(() => {
        button.classList.remove('added');
        button.innerHTML = '<i class="fas fa-plus"></i>';
    }, 1000);
    
    // Анимация перелета в корзину
    animateAddToCart(button);
    
    // Добавляем товар в корзину
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            quantity: 1
        });
    }
    
    updateCartDisplay();
}
// Анимация добавления в корзину
function animateAddToCart(button) {
    const buttonRect = button.getBoundingClientRect();
    const cartIcon = document.getElementById('cart-icon');
    const cartIconRect = cartIcon.getBoundingClientRect();
    
    // Позиционируем анимацию
    addToCartAnimation.style.left = `${buttonRect.left + buttonRect.width / 2}px`;
    addToCartAnimation.style.top = `${buttonRect.top + buttonRect.height / 2}px`;
    addToCartAnimation.style.fontSize = '20px';
    
    // Запускаем анимацию
    addToCartAnimation.classList.add('animating');
    
    // Анимация полета в корзину
    setTimeout(() => {
        addToCartAnimation.style.left = `${cartIconRect.left + cartIconRect.width / 2}px`;
        addToCartAnimation.style.top = `${cartIconRect.top + cartIconRect.height / 2}px`;
        addToCartAnimation.style.fontSize = '14px';
        addToCartAnimation.style.opacity = '0';
    }, 10);
    
    // Убираем анимацию после завершения
    setTimeout(() => {
        addToCartAnimation.classList.remove('animating');
        addToCartAnimation.style.opacity = '1';
    }, 600);
}
// Удаление товара из корзины
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartDisplay();
}
// Изменение количества товара
function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(productId);
    } else {
        updateCartDisplay();
    }
}
// Форматирование цены
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(price);
}
// Получение названия категории
function getCategoryName(category) {
    const names = {
        electronics: 'Электроника',
        furniture: 'Мебель',
        accessories: 'Аксессуары'
    };
    return names[category] || category;
}
// Оформление заказа - следующий шаг
function goToNextStep() {
    if (currentCheckoutStep >= 4) return;
    
    // Валидация текущего шага
    if (!validateStep(currentCheckoutStep)) {
        return;
    }
    
    // Сохранение данных текущего шага
    saveStepData(currentCheckoutStep);
    
    // Переход к следующему шагу
    currentCheckoutStep++;
    updateCheckoutSteps();
}
// Оформление заказа - предыдущий шаг
function goToPrevStep() {
    if (currentCheckoutStep <= 1) return;
    currentCheckoutStep--;
    updateCheckoutSteps();
}
// Обновление отображения шагов оформления заказа
function updateCheckoutSteps() {
    // Обновление визуального состояния шагов
    checkoutSteps.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        
        if (index + 1 < currentCheckoutStep) {
            step.classList.add('completed');
        } else if (index + 1 === currentCheckoutStep) {
            step.classList.add('active');
        }
    });
    
    // Показать соответствующий форму
    Object.values(checkoutForms).forEach(form => {
        form.style.display = 'none';
    });
    
    switch(currentCheckoutStep) {
        case 1:
            checkoutForms.info.style.display = 'block';
            break;
        case 2:
            checkoutForms.shipping.style.display = 'block';
            break;
        case 3:
            checkoutForms.payment.style.display = 'block';
            break;
        case 4:
            checkoutForms.confirm.style.display = 'block';
            renderOrderReview();
            break;
    }
}
// Валидация шага оформления заказа
function validateStep(step) {
    switch(step) {
        case 1:
            const firstName = document.getElementById('first-name').value.trim();
            const lastName = document.getElementById('last-name').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            
            if (!firstName || !lastName || !email || !phone) {
                alert('Пожалуйста, заполните все поля');
                return false;
            }
            
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                alert('Пожалуйста, введите корректный email');
                return false;
            }
            
            return true;
            
        case 2:
            const address = document.getElementById('address').value.trim();
            const city = document.getElementById('city').value.trim();
            const zip = document.getElementById('zip').value.trim();
            
            if (!address || !city || !zip) {
                alert('Пожалуйста, заполните все поля адреса');
                return false;
            }
            
            return true;
            
        case 3:
            const cardNumber = document.getElementById('card-number').value.trim();
            const cardExpiry = document.getElementById('card-expiry').value.trim();
            const cardCvc = document.getElementById('card-cvc').value.trim();
            const cardName = document.getElementById('card-name').value.trim();
            
            if (!cardNumber || !cardExpiry || !cardCvc || !cardName) {
                alert('Пожалуйста, заполните все данные карты');
                return false;
            }
            
            if (!/^\d{16}$/.test(cardNumber.replace(/\s/g, ''))) {
                alert('Номер карты должен содержать 16 цифр');
                return false;
            }
            
            if (!/^\d{2}\/\d{2}$/.test(cardExpiry)) {
                alert('Срок действия должен быть в формате MM/ГГ');
                return false;
            }
            
            if (!/^\d{3}$/.test(cardCvc)) {
                alert('CVC должен содержать 3 цифры');
                return false;
            }
            
            return true;
            
        default:
            return true;
    }
}
// Сохранение данных шага
function saveStepData(step) {
    switch(step) {
        case 1:
            orderData.firstName = document.getElementById('first-name').value.trim();
            orderData.lastName = document.getElementById('last-name').value.trim();
            orderData.email = document.getElementById('email').value.trim();
            orderData.phone = document.getElementById('phone').value.trim();
            break;
            
        case 2:
            orderData.address = document.getElementById('address').value.trim();
            orderData.city = document.getElementById('city').value.trim();
            orderData.zip = document.getElementById('zip').value.trim();
            orderData.shippingMethod = document.getElementById('shipping-method').value;
            break;
            
        case 3:
            orderData.cardNumber = document.getElementById('card-number').value.trim();
            orderData.cardExpiry = document.getElementById('card-expiry').value.trim();
            orderData.cardName = document.getElementById('card-name').value.trim();
            break;
    }
}
// Рендер обзора заказа
function renderOrderReview() {
    const subtotal = cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.id);
        return sum + (product.price * item.quantity);
    }, 0);
    
    let shipping = 0;
    if (subtotal > 0 && subtotal < 10000) {
        shipping = 300;
    }
    
    if (orderData.shippingMethod === 'express') {
        shipping = 700;
    } else if (orderData.shippingMethod === 'pickup') {
        shipping = 0;
    }
    
    const total = subtotal + shipping;
    
    const orderReview = document.getElementById('order-review');
    orderReview.innerHTML = `
        <div class="order-row">
            <span>Контактная информация:</span>
            <span>${orderData.firstName} ${orderData.lastName}</span>
        </div>
        <div class="order-row">
            <span>Email:</span>
            <span>${orderData.email}</span>
        </div>
        <div class="order-row">
            <span>Телефон:</span>
            <span>${orderData.phone}</span>
        </div>
        <div class="order-row">
            <span>Адрес доставки:</span>
            <span>${orderData.address}, ${orderData.city}</span>
        </div>
        <div class="order-row">
            <span>Способ доставки:</span>
            <span>${getShippingMethodName(orderData.shippingMethod)}</span>
        </div>
        <div class="order-row">
            <span>Товары:</span>
            <span>${formatPrice(subtotal)}</span>
        </div>
        <div class="order-row">
            <span>Доставка:</span>
            <span>${formatPrice(shipping)}</span>
        </div>
        <div class="order-row" style="font-weight: 600; font-size: 1.1rem;">
            <span>Итого:</span>
            <span>${formatPrice(total)}</span>
        </div>
    `;
}
// Получение названия способа доставки
function getShippingMethodName(method) {
    const methods = {
        standard: 'Стандартная (3-5 дней)',
        express: 'Экспресс (1-2 дня)',
        pickup: 'Самовывоз'
    };
    return methods[method] || method;
}
// Размещение заказа
function placeOrder() {
    // В реальном приложении здесь была бы отправка данных на сервер
    
    // Генерация номера заказа
    const orderId = 'ORD' + Date.now().toString().substring(7);
    orderData.orderId = orderId;
    orderData.date = new Date().toLocaleDateString('ru-RU');
    
    // Подсчет итоговой суммы
    const subtotal = cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.id);
        return sum + (product.price * item.quantity);
    }, 0);
    
    let shipping = 0;
    if (subtotal > 0 && subtotal < 10000) {
        shipping = 300;
    }
    
    if (orderData.shippingMethod === 'express') {
        shipping = 700;
    } else if (orderData.shippingMethod === 'pickup') {
        shipping = 0;
    }
    
    orderData.total = subtotal + shipping;
    
    // Отображение подтверждения
    renderOrderConfirmation();
    
    // Очистка корзины
    cart = [];
    updateCartDisplay();
    
    // Переход на страницу подтверждения
    navigateToPage('confirmation');
}
// Рендер подтверждения заказа
function renderOrderConfirmation() {
    const orderDetails = document.getElementById('order-details');
    orderDetails.innerHTML = `
        <h3>Детали заказа</h3>
        <div class="order-row">
            <span>Номер заказа:</span>
            <span>${orderData.orderId}</span>
        </div>
        <div class="order-row">
            <span>Дата:</span>
            <span>${orderData.date}</span>
        </div>
        <div class="order-row">
            <span>Имя:</span>
            <span>${orderData.firstName} ${orderData.lastName}</span>
        </div>
        <div class="order-row">
            <span>Email:</span>
            <span>${orderData.email}</span>
        </div>
        <div class="order-row">
            <span>Адрес доставки:</span>
            <span>${orderData.address}, ${orderData.city}</span>
        </div>
        <div class="order-row">
            <span>Способ доставки:</span>
            <span>${getShippingMethodName(orderData.shippingMethod)}</span>
        </div>
        <div class="order-row" style="font-weight: 600; font-size: 1.1rem;">
            <span>Итого:</span>
            <span>${formatPrice(orderData.total)}</span>
        </div>
    `;
}
// Настройка обработчиков событий
function setupEventListeners() {
    // Навигация
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageId = link.dataset.page;
            navigateToPage(pageId);
        });
    });
    
    // Мобильное меню
    mobileMenuBtn.addEventListener('click', () => {
        navLinksContainer.classList.toggle('active');
    });
    
    // Фильтры товаров
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderProducts(btn.dataset.filter, searchInput.value);
        });
    });
    
    // Поиск товаров
    searchInput.addEventListener('input', () => {
        const activeFilter = document.querySelector('.filter-btn.active');
        renderProducts(activeFilter.dataset.filter, searchInput.value);
    });
    
    // Добавление в корзину (делегирование событий)
    document.addEventListener('click', (e) => {
        // Кнопка добавления в корзину на главной
        if (e.target.closest('.add-to-cart-btn')) {
            const button = e.target.closest('.add-to-cart-btn');
            const productId = parseInt(button.dataset.id);
            addToCart(productId, button);
        }
        
        // Увеличение количества в корзине
        if (e.target.closest('.increase-quantity')) {
            const button = e.target.closest('.increase-quantity');
            const productId = parseInt(button.dataset.id);
            updateQuantity(productId, 1);
        }
        
        // Уменьшение количества в корзине
        if (e.target.closest('.decrease-quantity')) {
            const button = e.target.closest('.decrease-quantity');
            const productId = parseInt(button.dataset.id);
            updateQuantity(productId, -1);
        }
        
        // Удаление из корзины
        if (e.target.closest('.remove-item-btn')) {
            const button = e.target.closest('.remove-item-btn');
            const productId = parseInt(button.dataset.id);
            removeFromCart(productId);
        }
    });
    
    // Оформление заказа - кнопки навигации
    document.getElementById('checkout-btn')?.addEventListener('click', () => {
        if (cart.length === 0) {
            alert('Добавьте товары в корзину перед оформлением заказа');
            return;
        }
        navigateToPage('checkout');
        currentCheckoutStep = 1;
        updateCheckoutSteps();
    });
    
    // Оформление заказа - шаги
    document.getElementById('next-to-shipping')?.addEventListener('click', goToNextStep);
    document.getElementById('next-to-payment')?.addEventListener('click', goToNextStep);
    document.getElementById('next-to-confirm')?.addEventListener('click', goToNextStep);
    document.getElementById('back-to-info')?.addEventListener('click', goToPrevStep);
    document.getElementById('back-to-shipping')?.addEventListener('click', goToPrevStep);
    document.getElementById('back-to-payment')?.addEventListener('click', goToPrevStep);
    
    // Размещение заказа
    document.getElementById('place-order')?.addEventListener('click', placeOrder);
    
    // Ссылки в футере
    document.querySelectorAll('.footer-section a[data-filter]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const filter = link.dataset.filter;
            
            // Навигация на главную
            navigateToPage('home');
            
            // Установка активного фильтра
            setTimeout(() => {
                filterBtns.forEach(b => b.classList.remove('active'));
                document.querySelector(`.filter-btn[data-filter="${filter}"]`).classList.add('active');
                renderProducts(filter, searchInput.value);
            }, 300);
        });
    });
    
    // Обработка hash изменения для SPA навигации
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash.substring(1);
        if (hash && document.getElementById(hash)) {
            navigateToPage(hash);
        }
    });
}
// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', init);