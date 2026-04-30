// 3Dprint MD — catalog.js (Django version, fixed)

let productDatabase = {};
let currentProductData = null;
let currentProductKey = null;
let currentImageIndex = 0;
let currentGenreFilter = 'all';

// Рендер изображения: если это URL — делаем <img>, иначе текст
function renderImage(src, cls = '') {
    if (!src) return '<div class="product-image-placeholder">📦</div>';
    if (src.startsWith('/') || src.startsWith('http')) {
        return `<img src="${src}" class="product-img ${cls}" alt="Фото продукта" onerror="this.parentElement.innerHTML='📦'">`;
    }
    return `<span style="font-size:3rem">${src}</span>`;
}

// Загрузка продуктов из Django API
async function loadProducts() {
    try {
        await loadGenres();
        const res = await fetch('/api/products');
        productDatabase = await res.json();
        renderCards();
    } catch(e) {
        console.error('Ошибка загрузки продуктов:', e);
        document.getElementById('productsGrid').innerHTML =
            '<p style="color:#f87;text-align:center;padding:2rem;">Ошибка загрузки. Проверьте консоль.</p>';
    }
}

// Жанры загружаются из API — { slug: name }
let genreMap = {};

async function loadGenres() {
    try {
        const res = await fetch('/api/genres');
        const genres = await res.json();
        genreMap = {};
        genres.forEach(g => { genreMap[g.slug] = g.name; });
        renderGenreButtons();
    } catch(e) {
        console.error('Ошибка загрузки жанров:', e);
    }
}

function renderGenreButtons() {
    const container = document.querySelector('.genre-filter');
    if (!container) return;
    // Оставляем кнопку "Все", добавляем остальные динамически
    const allBtn = container.querySelector('[onclick*="all"]');
    container.innerHTML = '';
    if (allBtn) container.appendChild(allBtn);
    Object.entries(genreMap).forEach(([slug, name]) => {
        const btn = document.createElement('button');
        btn.className = 'genre-btn';
        btn.textContent = name;
        btn.onclick = function() { selectGenre(this, slug); };
        container.appendChild(btn);
    });
}

function getGenreLabel(genre) {
    return genreMap[genre] || genre;
}

function getSizeCategory(size) {
    const match = size.match(/(\d+)/);
    if (!match) return 'medium';
    const n = parseInt(match[1]);
    if (n < 10) return 'small';
    if (n <= 15) return 'medium';
    return 'large';
}

function renderCards() {
    const grid = document.getElementById('productsGrid');
    const sortVal  = document.getElementById('sortFilter')?.value || 'popular';
    const priceVal = document.getElementById('priceFilter')?.value || 'all';
    const sizeVal  = document.getElementById('sizeFilter')?.value  || 'all';

    let entries = Object.entries(productDatabase);

    if (currentGenreFilter !== 'all') {
        entries = entries.filter(([, p]) => p.genre === currentGenreFilter);
    }
    if (priceVal !== 'all') {
        if (priceVal === '0-300')   entries = entries.filter(([, p]) => p.price < 300);
        if (priceVal === '300-400') entries = entries.filter(([, p]) => p.price >= 300 && p.price <= 400);
        if (priceVal === '400+')    entries = entries.filter(([, p]) => p.price > 400);
    }
    if (sizeVal !== 'all') {
        entries = entries.filter(([, p]) => getSizeCategory(p.size) === sizeVal);
    }
    if (sortVal === 'price-low')  entries.sort((a, b) => a[1].price - b[1].price);
    if (sortVal === 'price-high') entries.sort((a, b) => b[1].price - a[1].price);
    if (sortVal === 'name')       entries.sort((a, b) => a[1].name.localeCompare(b[1].name));
    if (sortVal === 'popular')    entries.sort((a, b) => (b[1].featured ? 1 : 0) - (a[1].featured ? 1 : 0));

    document.getElementById('resultsCount').textContent = entries.length;

    if (entries.length === 0) {
        grid.innerHTML = '<p style="color:#aaa;text-align:center;padding:2rem;">Продуктов не найдено</p>';
        return;
    }

    grid.innerHTML = entries.map(([key, p]) => `
        <div class="product-card" data-genre="${p.genre}" data-price="${p.price}" data-size="${getSizeCategory(p.size)}" data-product-key="${key}">
            <div class="product-image">
                ${renderImage(p.images[0], 'card-img')}
            </div>
            <div class="product-info">
                <span class="product-tag">${p.genreName || getGenreLabel(p.genre)}</span>
                <h3 class="product-name">${p.name}</h3>
                <p class="product-description">${p.description.substring(0, 70)}...</p>
                <div class="product-meta">
                    <div class="meta-item"><span>📏</span><span>${p.size}</span></div>
                    <div class="meta-item"><span>⏱️</span><span>${p.time}</span></div>
                </div>
                <div class="product-footer">
                    <span class="price">${p.price} MDL</span>
                    <button class="order-btn" onclick="event.stopPropagation(); openProductDetailModal('${key}')">Заказать</button>
                </div>
            </div>
        </div>
    `).join('');

    grid.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.classList.contains('order-btn')) return;
            openProductDetailModal(card.getAttribute('data-product-key'));
        });
    });
}

function applyFilters() { renderCards(); }

function selectGenre(btn, genre) {
    document.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentGenreFilter = genre;
    renderCards();
}

function resetFilters() {
    document.getElementById('sortFilter').value = 'popular';
    document.getElementById('priceFilter').value = 'all';
    document.getElementById('sizeFilter').value = 'all';
    currentGenreFilter = 'all';
    document.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.genre-btn')?.classList.add('active');
    renderCards();
}

function openProductDetailModal(key) {
    const p = productDatabase[key];
    if (!p) return;
    currentProductData = p;
    currentProductKey = key;
    currentImageIndex = 0;

    document.getElementById('productDetailTitle').textContent = p.name;
    document.getElementById('productDetailPrice').textContent = p.price + ' MDL';
    document.getElementById('productMaterial').textContent = p.material;
    document.getElementById('productSize').textContent = p.size;
    document.getElementById('productTime').textContent = p.time;
    document.getElementById('productColors').textContent = p.colors;
    document.getElementById('productDetailDescription').textContent = p.description;

    // Главное фото
    const mainImg = document.getElementById('productDetailMainImage');
    mainImg.innerHTML = p.images.length > 0
        ? renderImage(p.images[0], 'detail-img')
        : '<span style="font-size:4rem">📦</span>';

    // Миниатюры
    const thumbs = document.getElementById('productThumbnails');
    thumbs.innerHTML = p.images.map((img, i) =>
        `<div class="gallery-thumbnail${i===0?' active':''}" onclick="setProductImage(${i})">
            ${renderImage(img, 'thumb-img')}
        </div>`
    ).join('');

    document.getElementById('productDetailModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function changeProductImage(dir) {
    if (!currentProductData || !currentProductData.images.length) return;
    currentImageIndex = (currentImageIndex + dir + currentProductData.images.length) % currentProductData.images.length;
    setProductImage(currentImageIndex);
}

function setProductImage(index) {
    if (!currentProductData) return;
    currentImageIndex = index;
    const mainImg = document.getElementById('productDetailMainImage');
    mainImg.innerHTML = renderImage(currentProductData.images[index], 'detail-img');
    document.querySelectorAll('.gallery-thumbnail').forEach((t, i) => t.classList.toggle('active', i === index));
}

function closeAllModals() {
    document.getElementById('productDetailModal').classList.remove('active');
    document.getElementById('productModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function orderFromDetail() {
    if (!currentProductData) return;
    closeAllModals();
    openOrderModal(currentProductKey);
}

function openOrderModal(key) {
    const p = productDatabase[key];
    if (!p) return;
    currentProductKey = key;
    document.getElementById('productName').value = key;

    // Превью в модалке заказа
    const previewEmoji = document.getElementById('productPreviewEmoji');
    previewEmoji.innerHTML = p.images.length > 0
        ? renderImage(p.images[0], 'preview-img')
        : '📦';

    document.getElementById('productPreviewName').textContent = p.name;
    document.getElementById('productPreviewPrice').textContent = p.price;

    // Блок выбора фото — показываем только если есть selectable фото
    const photoGroup = document.getElementById('photoChoiceGroup');
    const photoGrid  = document.getElementById('photoChoiceGrid');
    const chosenInput = document.getElementById('chosenPhoto');
    chosenInput.value = '';

    const selectable = p.selectableImages || [];
    if (selectable.length > 0) {
        photoGroup.style.display = 'block';
        photoGrid.innerHTML = selectable.map((url, i) => `
            <div class="photo-choice-item" onclick="selectPhoto(this, '${url}')" style="
                cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;
                transition:border-color 0.2s,transform 0.2s;aspect-ratio:1/1;
            ">
                <img src="${url}" style="width:100%;height:100%;object-fit:cover;" alt="Вариант ${i+1}">
            </div>
        `).join('');
    } else {
        photoGroup.style.display = 'none';
        photoGrid.innerHTML = '';
    }

    updateProductPrice();
    document.getElementById('productModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function selectPhoto(el, url) {
    // Снимаем выделение со всех
    document.querySelectorAll('.photo-choice-item').forEach(item => {
        item.style.borderColor = 'transparent';
        item.style.transform = 'scale(1)';
    });
    // Выделяем выбранное
    el.style.borderColor = '#00f0ff';
    el.style.transform = 'scale(1.05)';
    document.getElementById('chosenPhoto').value = url;
}

function updateProductPrice() {
    const p = productDatabase[currentProductKey];
    if (!p) return;
    let total = p.price;
    if (document.getElementById('productColor').value === 'multicolor') total += 150;
    if (document.getElementById('productFill').value === 'solid') total += 100;
    document.getElementById('productPrice').textContent = total;
}

async function submitOrder(event) {
    event.preventDefault();
    const payload = {
        productKey:  document.getElementById('productName').value,
        color:       document.getElementById('productColor').value,
        fill:        document.getElementById('productFill').value,
        name:        document.getElementById('customerName').value,
        phone:       document.getElementById('customerPhone').value,
        address:     document.getElementById('customerAddress').value,
        notes:       document.getElementById('customerNotes').value,
        totalPrice:  parseInt(document.getElementById('productPrice').textContent),
        chosenPhoto: document.getElementById('chosenPhoto')?.value || '',
    };

    try {
        const res = await fetch('/api/order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (data.ok) {
            alert(`✅ Заказ #${data.orderId} принят!\n\nТовар: ${productDatabase[payload.productKey]?.name}\nИтого: ${payload.totalPrice} MDL\n\nМы свяжемся с вами для подтверждения.`);
            closeAllModals();
            document.getElementById('productForm').reset();
        } else {
            alert('Ошибка: ' + data.error);
        }
    } catch(e) {
        alert('Ошибка соединения: ' + e.message);
    }
}

document.addEventListener('DOMContentLoaded', loadProducts);
