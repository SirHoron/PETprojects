// Initial book data
const initialBooks = [
    {
        id: 0,
        title: "Мастер и Маргарита",
        author: "Михаил Булгаков",
        genre: "Роман",
        status: "read",
        rating: 5,
        notes: "Великолепная книга, перечитываю каждый год"
    },
    {
        id: 1,
        title: "1984",
        author: "Джордж Оруэлл",
        genre: "Фантастика",
        status: "read",
        rating: 5,
        notes: "Актуально как никогда"
    },
    {
        id: 2,
        title: "Преступление и наказание",
        author: "Фёдор Достоевский",
        genre: "Роман",
        status: "read",
        rating: 4,
        notes: "Тяжелое, но гениальное произведение"
    },
    {
        id: 3,
        title: "Гарри Поттер и философский камень",
        author: "Джоан Роулинг",
        genre: "Фэнтези",
        status: "read",
        rating: 5,
        notes: ""
    },
    {
        id: 4,
        title: "Убийство в Восточном экспрессе",
        author: "Агата Кристи",
        genre: "Детектив",
        status: "read",
        rating: 4,
        notes: "Гениальная развязка"
    },
    {
        id: 5,
        title: "Семь навыков высокоэффективных людей",
        author: "Стивен Кови",
        genre: "Нон-фикшн",
        status: "reading",
        rating: 3,
        notes: "Читаю для саморазвития"
    },
    {
        id: 6,
        title: "Атлант расправил плечи",
        author: "Айн Рэнд",
        genre: "Фантастика",
        status: "reading",
        rating: 3,
        notes: "Очень объемная, но интересная"
    },
    {
        id: 7,
        title: "Шерлок Холмс: Сборник рассказов",
        author: "Артур Конан Дойл",
        genre: "Детектив",
        status: "read",
        rating: 4,
        notes: ""
    },
    {
        id: 8,
        title: "Война и мир",
        author: "Лев Толстой",
        genre: "Роман",
        status: "reading",
        rating: 4,
        notes: "Читаю медленно, но верно"
    },
    {
        id: 9,
        title: "Дюна",
        author: "Фрэнк Герберт",
        genre: "Фантастика",
        status: "read",
        rating: 4,
        notes: "Отличная научная фантастика"
    },
    {
        id: 10,
        title: "Маленький принц",
        author: "Антуан де Сент-Экзюпери",
        genre: "Фантастика",
        status: "read",
        rating: 5,
        notes: "Философская сказка для всех возрастов"
    }
];
let books = [...initialBooks];
let nextId = initialBooks.length + 1;
// DOM elements
const booksGrid = document.getElementById('books-grid');
const addBookBtn = document.getElementById('add-book-btn');
const modalOverlay = document.getElementById('modal-overlay');
const closeModal = document.getElementById('close-modal');
const cancelBtn = document.getElementById('cancel-btn');
const addBookForm = document.getElementById('add-book-form');
const ratingStars = document.querySelectorAll('.rating-star');
const ratingValue = document.getElementById('rating-value');
const bookRatingInput = document.getElementById('book-rating');
const resetFiltersBtn = document.getElementById('reset-filters');
const noResults = document.getElementById('no-results');
const totalBooksElement = document.getElementById('total-books');
const readBooksElement = document.getElementById('read-books');
const avgRatingElement = document.getElementById('avg-rating');
// Current filters
let activeFilters = {
    status: ['read', 'reading', 'plan'],
    rating: [],
    genre: ['Фантастика', 'Роман', 'Детектив', 'Нон-фикшн']
};
// Initialize the app
function init() {
    renderBooks();
    updateStats();
    setupEventListeners();
}
// Render books to the grid
function renderBooks() {
    const filteredBooks = filterBooks();
    
    if (filteredBooks.length === 0) {
        booksGrid.style.display = 'none';
        noResults.style.display = 'block';
    } else {
        booksGrid.style.display = 'grid';
        noResults.style.display = 'none';
        
        booksGrid.innerHTML = '';
        
        filteredBooks.forEach(book => {
            const bookCard = createBookCard(book);
            booksGrid.appendChild(bookCard);
        });
    }
    
    updateFilterCounts();
}
// Create a book card element
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.dataset.id = book.id;
    
    // Status class
    const statusClass = `status-${book.status}`;
    const statusText = book.status === 'read' ? 'Прочитано' : 
                     book.status === 'reading' ? 'Читаю сейчас' : 'Планирую';
    
    // Generate star rating HTML
    let starsHtml = '';
    if (book.rating > 0) {
        for (let i = 1; i <= 5; i++) {
            if (i <= book.rating) {
                starsHtml += '<i class="fas fa-star"></i>';
            } else {
                starsHtml += '<i class="far fa-star"></i>';
            }
        }
    }
    
    card.innerHTML = `
        <div class="book-cover">
            ${book.rating > 0 ? `<div class="book-rating">${starsHtml}</div>` : ''}
            <div class="book-cover-placeholder">
                <i class="fas fa-book"></i>
                <span>${book.genre}</span>
            </div>
        </div>
        <div class="book-info">
            <h3 class="book-title">${book.title}</h3>
            <p class="book-author">${book.author}</p>
            <div class="book-genres">
                <span class="genre-tag">${book.genre}</span>
            </div>
            <div class="book-actions">
                <span class="book-status ${statusClass}">${statusText}</span>
                <button class="delete-book" data-id="${book.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    return card;
}
// Filter books based on active filters
function filterBooks() {
    return books.filter(book => {
        // Check status filter
        if (activeFilters.status.length > 0 && !activeFilters.status.includes(book.status)) {
            return false;
        }
        
        // Check rating filter
        if (activeFilters.rating.length > 0 && book.rating > 0) {
            if (!activeFilters.rating.includes(book.rating.toString())) {
                return false;
            }
        }
        
        // Check genre filter
        if (activeFilters.genre.length > 0 && !activeFilters.genre.includes(book.genre)) {
            return false;
        }
        
        return true;
    });
}
// Update filter counts based on current books
function updateFilterCounts() {
    // Update status counts
    const readCount = books.filter(b => b.status === 'read').length;
    const readingCount = books.filter(b => b.status === 'reading').length;
    const planCount = books.filter(b => b.status === 'plan').length;
    
    document.querySelector('.filter-option[data-value="read"] .count').textContent = readCount;
    document.querySelector('.filter-option[data-value="reading"] .count').textContent = readingCount;
    document.querySelector('.filter-option[data-value="plan"] .count').textContent = planCount;
    
    // Update rating counts
    const rating5Count = books.filter(b => b.rating === 5).length;
    const rating4Count = books.filter(b => b.rating === 4).length;
    const rating3Count = books.filter(b => b.rating === 3).length;
    const rating2Count = books.filter(b => b.rating === 2).length;
    const rating1Count = books.filter(b => b.rating === 1).length;
    
    document.querySelector('.filter-option[data-value="5"] .count').textContent = rating5Count;
    document.querySelector('.filter-option[data-value="4"] .count').textContent = rating4Count;
    document.querySelector('.filter-option[data-value="3"] .count').textContent = rating3Count;
    document.querySelector('.filter-option[data-value="2"] .count').textContent = rating2Count;
    document.querySelector('.filter-option[data-value="1"] .count').textContent = rating1Count;
    
    // Update genre counts
    const genres = ['Фантастика', 'Роман', 'Детектив', 'Нон-фикшн'];
    genres.forEach(genre => {
        const count = books.filter(b => b.genre === genre).length;
        const element = document.querySelector(`.filter-option[data-value="${genre}"] .count`);
        if (element) {
            element.textContent = count;
        }
    });
}
// Update statistics
function updateStats() {
    totalBooksElement.textContent = books.length;
    
    const readBooks = books.filter(b => b.status === 'read').length;
    readBooksElement.textContent = readBooks;
    
    const ratedBooks = books.filter(b => b.rating > 0);
    if (ratedBooks.length > 0) {
        const avgRating = ratedBooks.reduce((sum, book) => sum + book.rating, 0) / ratedBooks.length;
        avgRatingElement.textContent = avgRating.toFixed(1);
    } else {
        avgRatingElement.textContent = '0.0';
    }
}
// Setup event listeners
function setupEventListeners() {
    // Add book button
    addBookBtn.addEventListener('click', () => {
        modalOverlay.style.display = 'flex';
    });
    
    // Close modal buttons
    closeModal.addEventListener('click', closeModalFunc);
    cancelBtn.addEventListener('click', closeModalFunc);
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModalFunc();
        }
    });
    
    // Rating stars
    ratingStars.forEach(star => {
        star.addEventListener('click', () => {
            const value = parseInt(star.dataset.value);
            setRating(value);
        });
    });
    
    // Form submission
    addBookForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addNewBook();
    });
    
    // Filter checkboxes
    document.querySelectorAll('.filter-option input').forEach(checkbox => {
        checkbox.addEventListener('change', updateFilters);
    });
    
    // Reset filters button
    resetFiltersBtn.addEventListener('click', resetFilters);
    
    // Delete book buttons (event delegation)
    document.addEventListener('click', (e) => {
        if (e.target.closest('.delete-book')) {
            const bookId = parseInt(e.target.closest('.delete-book').dataset.id);
            deleteBook(bookId);
        }
    });
}
// Close modal function
function closeModalFunc() {
    modalOverlay.style.display = 'none';
    addBookForm.reset();
    setRating(0);
    
    // Clear error messages
    document.querySelectorAll('.error-message').forEach(error => {
        error.classList.remove('show');
    });
}
// Set rating stars
function setRating(value) {
    ratingStars.forEach(star => {
        const starValue = parseInt(star.dataset.value);
        if (starValue <= value) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    
    ratingValue.textContent = value;
    bookRatingInput.value = value;
}
// Add new book
function addNewBook() {
    const title = document.getElementById('book-title').value.trim();
    const author = document.getElementById('book-author').value.trim();
    const genre = document.getElementById('book-genre').value;
    const status = document.getElementById('book-status').value;
    const rating = parseInt(bookRatingInput.value);
    const notes = document.getElementById('book-notes').value.trim();
    
    // Validate
    let isValid = true;
    
    if (!title) {
        document.getElementById('title-error').classList.add('show');
        isValid = false;
    } else {
        document.getElementById('title-error').classList.remove('show');
    }
    
    if (!author) {
        document.getElementById('author-error').classList.add('show');
        isValid = false;
    } else {
        document.getElementById('author-error').classList.remove('show');
    }
    
    if (!isValid) return;
    
    // Add new book
    const newBook = {
        id: nextId++,
        title,
        author,
        genre,
        status,
        rating,
        notes
    };
    
    books.push(newBook);
    renderBooks();
    updateStats();
    closeModalFunc();
    
    // Show success message (in a real app, you might want a toast notification)
    alert(`Книга "${title}" успешно добавлена в вашу библиотеку!`);
}
// Delete book
function deleteBook(id) {
    if (confirm('Вы уверены, что хотите удалить эту книгу из библиотеки?')) {
        books = books.filter(book => book.id !== id);
        renderBooks();
        updateStats();
    }
}
// Update filters based on checkbox states
function updateFilters() {
    activeFilters = {
        status: [],
        rating: [],
        genre: []
    };
    
    // Get all checked checkboxes
    document.querySelectorAll('.filter-option input:checked').forEach(checkbox => {
        const filterOption = checkbox.closest('.filter-option');
        const filterType = filterOption.dataset.filter;
        const filterValue = filterOption.dataset.value;
        
        if (activeFilters[filterType]) {
            activeFilters[filterType].push(filterValue);
        }
    });
    
    renderBooks();
}
// Reset all filters
function resetFilters() {
    // Check all checkboxes
    document.querySelectorAll('.filter-option input').forEach(checkbox => {
        checkbox.checked = true;
    });
    
    // Reset active filters
    activeFilters = {
        status: ['read', 'reading', 'plan'],
        rating: ['5', '4', '3', '2'],
        genre: ['Фантастика', 'Роман', 'Детектив', 'Нон-фикшн']
    };
    
    renderBooks();
}
// Initialize the application
document.addEventListener('DOMContentLoaded', init);