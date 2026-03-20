// products.js — база товаров
// Данные встроены напрямую (fallback), и обновляются с API если оно доступно

var productDatabase = {
  "Dragon Warrior": {
    "name": "Воин-Дракон", "price": 349, "genre": "fantasy", "featured": true,
    "material": "Фотополимерная смола", "size": "12-15 см", "time": "8-12 часов",
    "colors": "Серый, Многоцветный",
    "description": "Эпическая фэнтези-модель воина с детализированной драконьей броней.",
    "images": ["🐉", "⚔️", "🛡️", "👑"]
  },
  "Cyber Cat": {
    "name": "Кибер-Кот", "price": 299, "genre": "scifi", "featured": true,
    "material": "Фотополимерная смола", "size": "10-12 см", "time": "6-10 часов",
    "colors": "Серый, Многоцветный, LED подсветка",
    "description": "Футуристическая модель кибер-кота с возможностью установки LED-подсветки.",
    "images": ["🐱", "💡", "🤖", "✨"]
  },
  "Space Explorer": {
    "name": "Космический Исследователь", "price": 399, "genre": "scifi", "featured": true,
    "material": "Фотополимерная смола", "size": "15-18 см", "time": "10-14 часов",
    "colors": "Серый, Многоцветный",
    "description": "Детализированная фигурка астронавта с подвижными деталями.",
    "images": ["🚀", "👨‍🚀", "🌟", "🛸"]
  },
  "Mystic Wizard": {
    "name": "Мистический Маг", "price": 329, "genre": "fantasy", "featured": true,
    "material": "Фотополимерная смола", "size": "13-16 см", "time": "9-12 часов",
    "colors": "Серый, Многоцветный",
    "description": "Детализированный волшебник с магическими эффектами.",
    "images": ["🧙", "✨", "🔮", "📜"]
  },
  "Robo Buddy": {
    "name": "Робо-Друг", "price": 279, "genre": "cute", "featured": true,
    "material": "Фотополимерная смола", "size": "8-10 см", "time": "5-8 часов",
    "colors": "Серый, Многоцветный",
    "description": "Милый робот-компаньон с шарнирными соединениями.",
    "images": ["🤖", "💙", "⚙️", "🔧"]
  },
  "Skull Guardian": {
    "name": "Страж-Череп", "price": 349, "genre": "dark", "featured": true,
    "material": "Фотополимерная смола", "size": "12-14 см", "time": "8-11 часов",
    "colors": "Серый, Многоцветный",
    "description": "Мрачная и детализированная модель стража с черепом.",
    "images": ["💀", "⚔️", "🗡️", "⛓️"]
  }
};

// Попробовать загрузить актуальные данные с API
// Если API недоступен — используем встроенные данные выше
function loadProducts() {
    fetch('/api/products')
        .then(function(r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function(data) {
            productDatabase = data;
            if (typeof renderCarousel     === 'function') renderCarousel();
            if (typeof renderProductsGrid === 'function') renderProductsGrid();
        })
        .catch(function() {
            // API недоступен — рендерим встроенные данные
            if (typeof renderCarousel     === 'function') renderCarousel();
            if (typeof renderProductsGrid === 'function') renderProductsGrid();
        });
}
