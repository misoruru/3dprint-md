// modals.js — логика модальных окон заказа (общая для index и catalog)

let baseProductPrice = 0;

function openProductModal(productName, price, emoji) {
    baseProductPrice = parseInt(price);
    const nameEl = document.getElementById('productName');
    if (nameEl) nameEl.value = productName;

    const previewEmoji = document.getElementById('productPreviewEmoji');
    const previewName  = document.getElementById('productPreviewName');
    const previewPrice = document.getElementById('productPreviewPrice');
    if (previewEmoji) previewEmoji.textContent = emoji || '';
    if (previewName)  previewName.textContent  = productName;
    if (previewPrice) previewPrice.textContent  = price;

    const colorEl = document.getElementById('productColor');
    const fillEl  = document.getElementById('productFill');
    if (colorEl) colorEl.value = 'gray';
    if (fillEl)  fillEl.value  = 'lattice';

    updateProductPrice();
    document.getElementById('productModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function updateProductPrice() {
    const colorEl = document.getElementById('productColor');
    const fillEl  = document.getElementById('productFill');
    const priceEl = document.getElementById('productPrice');
    if (!colorEl || !fillEl || !priceEl) return;

    let total = baseProductPrice;
    if (colorEl.value === 'multicolor') total += 150;
    if (fillEl.value  === 'solid')      total += 100;
    priceEl.textContent = total;
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
    document.body.style.overflow = 'auto';
}

// Close on backdrop click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) closeAllModals();
});

// Close on Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeAllModals();
});
