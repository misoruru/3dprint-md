
        // Product Database with detailed information
        const productDatabase = {
            'Dragon Warrior': {
                name: 'Воин-Дракон',
                price: 349,
                material: 'Фотополимерная смола',
                size: '12-15 см',
                time: '8-12 часов',
                colors: 'Серый, Многоцветный',
                description: 'Эпическая фэнтези-модель воина с детализированной драконьей броней. Идеально подходит для коллекционеров и любителей настольных игр. Высокая детализация, прочная конструкция, возможность покраски.',
                images: ['🐉', '⚔️', '🛡️', '👑']
            },
            'Cyber Cat': {
                name: 'Кибер-Кот',
                price: 299,
                material: 'Фотополимерная смола',
                size: '10-12 см',
                time: '6-10 часов',
                colors: 'Серый, Многоцветный, LED подсветка',
                description: 'Футуристическая модель кибер-кота с возможностью установки LED-подсветки. Современный дизайн с технологическими деталями. Отличный подарок для любителей киберпанка и sci-fi.',
                images: ['🐱', '💡', '🤖', '✨']
            },
            'Space Explorer': {
                name: 'Космический Исследователь',
                price: 399,
                material: 'Фотополимерная смола',
                size: '15-18 см',
                time: '10-14 часов',
                colors: 'Серый, Многоцветный',
                description: 'Детализированная фигурка астронавта с подвижными деталями. Идеально подходит для любителей космоса и научной фантастики. Шарнирные соединения позволяют менять позу.',
                images: ['🚀', '👨‍🚀', '🌟', '🛸']
            },
            'Mystic Wizard': {
                name: 'Мистический Маг',
                price: 329,
                material: 'Фотополимерная смола',
                size: '13-16 см',
                time: '9-12 часов',
                colors: 'Серый, Многоцветный',
                description: 'Детализированный волшебник с магическими эффектами и развевающейся мантией. Отличное дополнение к коллекции фэнтези-миниатюр. Тщательно проработанные детали одежды и аксессуаров.',
                images: ['🧙', '✨', '🔮', '📜']
            },
            'Robo Buddy': {
                name: 'Робо-Друг',
                price: 279,
                material: 'Фотополимерная смола',
                size: '8-10 см',
                time: '5-8 часов',
                colors: 'Серый, Многоцветный',
                description: 'Милый робот-компаньон с шарнирными соединениями. Идеальный настольный сувенир или подарок для детей. Прочная конструкция, подвижные части.',
                images: ['🤖', '💙', '⚙️', '🔧']
            },
            'Skull Guardian': {
                name: 'Страж-Череп',
                price: 349,
                material: 'Фотополимерная смола',
                size: '12-14 см',
                time: '8-11 часов',
                colors: 'Серый, Многоцветный',
                description: 'Мрачная и детализированная модель стража с черепом. Отличное украшение для любителей готического стиля. Высокая детализация костей и доспехов.',
                images: ['💀', '⚔️', '🗡️', '⛓️']
            }
        };

        let currentProductData = null;
        let currentImageIndex = 0;
        let basePrice = 0;

        // Open Product Detail Modal
        function openProductDetailModal(productKey) {
            currentProductData = productDatabase[productKey];
            if (!currentProductData) return;

            currentImageIndex = 0;
            
            document.getElementById('productDetailTitle').textContent = currentProductData.name;
            document.getElementById('productDetailPrice').textContent = currentProductData.price + ' MDL';
            document.getElementById('productMaterial').textContent = currentProductData.material;
            document.getElementById('productSize').textContent = currentProductData.size;
            document.getElementById('productTime').textContent = currentProductData.time;
            document.getElementById('productColors').textContent = currentProductData.colors;
            document.getElementById('productDetailDescription').textContent = currentProductData.description;
            
            // Update main image
            document.getElementById('productDetailMainImage').textContent = currentProductData.images[0];
            
            // Create thumbnails
            const thumbnailsContainer = document.getElementById('productThumbnails');
            thumbnailsContainer.innerHTML = '';
            currentProductData.images.forEach((image, index) => {
                const thumb = document.createElement('div');
                thumb.className = 'gallery-thumbnail' + (index === 0 ? ' active' : '');
                thumb.textContent = image;
                thumb.onclick = () => setProductImage(index);
                thumbnailsContainer.appendChild(thumb);
            });
            
            document.getElementById('productDetailModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Open Order Form Modal
        function openOrderModal(productName, price, emoji) {
            basePrice = price;
            document.getElementById('productName').value = productName;
            document.getElementById('productColor').value = 'gray';
            document.getElementById('productFill').value = 'lattice';

            // Fill preview block
            document.getElementById('productPreviewName').textContent = productName;
            document.getElementById('productPreviewPrice').textContent = price;
            document.getElementById('productPreviewEmoji').textContent = emoji || '';

            updateProductPrice();
            
            document.getElementById('productModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Update product price based on selections
        function updateProductPrice() {
            let totalPrice = basePrice;
            
            const color = document.getElementById('productColor').value;
            const fill = document.getElementById('productFill').value;
            
            if (color === 'multicolor') {
                totalPrice += 150;
            }
            
            if (fill === 'solid') {
                totalPrice += 100;
            }
            
            document.getElementById('productPrice').textContent = totalPrice;
        }

        // Submit order form
        function submitOrder(event) {
            event.preventDefault();
            
            const formData = {
                product: document.getElementById('productName').value,
                color: document.getElementById('productColor').value,
                fill: document.getElementById('productFill').value,
                name: document.getElementById('customerName').value,
                phone: document.getElementById('customerPhone').value,
                address: document.getElementById('customerAddress').value,
                notes: document.getElementById('customerNotes').value,
                totalPrice: document.getElementById('productPrice').textContent
            };
            
            console.log('Order submitted:', formData);
            alert(`Заказ подтвержден!\n\nТовар: ${formData.product}\nИтого: ${formData.totalPrice} MDL\n\nМы свяжемся с вами в ближайшее время для оплаты и уточнения деталей.`);
            
            closeAllModals();
            document.getElementById('productForm').reset();
        }

        // Change product image (next/prev)
        function changeProductImage(direction) {
            if (!currentProductData) return;
            
            currentImageIndex += direction;
            if (currentImageIndex < 0) {
                currentImageIndex = currentProductData.images.length - 1;
            } else if (currentImageIndex >= currentProductData.images.length) {
                currentImageIndex = 0;
            }
            
            setProductImage(currentImageIndex);
        }

        // Set specific product image
        function setProductImage(index) {
            if (!currentProductData) return;
            
            currentImageIndex = index;
            document.getElementById('productDetailMainImage').textContent = currentProductData.images[index];
            
            // Update active thumbnail
            const thumbnails = document.querySelectorAll('.gallery-thumbnail');
            thumbnails.forEach((thumb, i) => {
                thumb.classList.toggle('active', i === index);
            });
        }

        // Close all modals
        function closeAllModals() {
            document.getElementById('productDetailModal').classList.remove('active');
            document.getElementById('productModal').classList.remove('active');
            document.body.style.overflow = 'auto';
        }

        // Order from detail page
        function orderFromDetail() {
            if (!currentProductData) return;
            
            // Close detail modal
            document.getElementById('productDetailModal').classList.remove('active');
            
            // Open order modal with emoji from product images
            const emoji = currentProductData.images ? currentProductData.images[0] : '';
            openOrderModal(currentProductData.name, currentProductData.price, emoji);
        }

        // Add click handlers to product cards
        document.addEventListener('DOMContentLoaded', function() {
            const productCards = document.querySelectorAll('.product-card');
            productCards.forEach(card => {
                card.addEventListener('click', function(e) {
                    if (!e.target.classList.contains('order-btn')) {
                        const productKey = card.getAttribute('data-product-key');
                        openProductDetailModal(productKey);
                    }
                });
                
                const orderBtn = card.querySelector('.order-btn');
                orderBtn.onclick = function(e) {
                    e.stopPropagation();
                    const productKey = card.getAttribute('data-product-key');
                    const productData = productDatabase[productKey];
                    const emoji = productData && productData.images ? productData.images[0] : '';
                    const productName = card.querySelector('.product-name').textContent;
                    const price = parseInt(card.getAttribute('data-price'));
                    openOrderModal(productName, price, emoji);
                };
            });
        });

        // Close modal on outside click
        document.addEventListener('click', function(event) {
            const detailModal = document.getElementById('productDetailModal');
            const orderModal = document.getElementById('productModal');
            
            if (event.target === detailModal || event.target === orderModal) {
                closeAllModals();
            }
        });

        // Close modal on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeAllModals();
            }
        });

        // ============================================
        // STARRY NIGHT BACKGROUND
        // ============================================
        const canvas = document.getElementById('starryCanvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        class Star {
            constructor() {
                this.reset();
                this.y = Math.random() * canvas.height;
                this.opacity = Math.random() * 0.5 + 0.3;
            }

            reset() {
                this.x = Math.random() * canvas.width;
                this.y = -10;
                this.size = Math.random() * 2 + 0.5;
                this.speed = Math.random() * 0.3 + 0.1;
                this.opacity = Math.random() * 0.5 + 0.3;
                this.twinkleSpeed = Math.random() * 0.02 + 0.01;
                this.twinklePhase = Math.random() * Math.PI * 2;
            }

            update(mouseX, mouseY) {
                this.twinklePhase += this.twinkleSpeed;
                this.opacity = 0.3 + Math.sin(this.twinklePhase) * 0.3;

                const dx = this.x - mouseX;
                const dy = this.y - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const maxDistance = 150;

                if (distance < maxDistance) {
                    const force = (maxDistance - distance) / maxDistance;
                    this.x += (dx / distance) * force * 2;
                    this.y += (dy / distance) * force * 2;
                }

                this.y += this.speed;

                if (this.y > canvas.height + 10) {
                    this.reset();
                }
                if (this.x < -10 || this.x > canvas.width + 10) {
                    this.x = Math.random() * canvas.width;
                }
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                
                const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 3);
                gradient.addColorStop(0, `rgba(0, 240, 255, ${this.opacity})`);
                gradient.addColorStop(0.5, `rgba(157, 78, 221, ${this.opacity * 0.3})`);
                gradient.addColorStop(1, 'rgba(0, 240, 255, 0)');
                
                ctx.fillStyle = gradient;
                ctx.fill();
            }
        }

        const stars = [];
        const starCount = 150;
        for (let i = 0; i < starCount; i++) {
            stars.push(new Star());
        }

        let mouseX = canvas.width / 2;
        let mouseY = canvas.height / 2;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            stars.forEach(star => {
                star.update(mouseX, mouseY);
                star.draw();
            });

            requestAnimationFrame(animate);
        }

        animate();

        // ============================================
        // FILTER FUNCTIONALITY
        // ============================================
        let currentGenre = 'all';
        let currentSort = 'popular';
        let currentPriceRange = 'all';
        let currentSize = 'all';

        function selectGenre(button, genre) {
            document.querySelectorAll('.genre-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            button.classList.add('active');
            currentGenre = genre;
            applyFilters();
        }

        function applyFilters() {
            currentSort = document.getElementById('sortFilter').value;
            currentPriceRange = document.getElementById('priceFilter').value;
            currentSize = document.getElementById('sizeFilter').value;

            const cards = Array.from(document.querySelectorAll('.product-card'));
            let visibleCount = 0;

            cards.forEach(card => {
                const cardGenre = card.getAttribute('data-genre');
                const cardPrice = parseInt(card.getAttribute('data-price'));
                const cardSize = card.getAttribute('data-size');

                let showCard = true;

                if (currentGenre !== 'all' && cardGenre !== currentGenre) {
                    showCard = false;
                }

                if (currentPriceRange !== 'all') {
                    if (currentPriceRange === '0-300' && cardPrice > 300) showCard = false;
                    if (currentPriceRange === '300-400' && (cardPrice < 300 || cardPrice > 400)) showCard = false;
                    if (currentPriceRange === '400+' && cardPrice < 400) showCard = false;
                }

                if (currentSize !== 'all' && cardSize !== currentSize) {
                    showCard = false;
                }

                if (showCard) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            const visibleCards = cards.filter(card => card.style.display !== 'none');
            
            if (currentSort === 'price-low') {
                visibleCards.sort((a, b) => parseInt(a.getAttribute('data-price')) - parseInt(b.getAttribute('data-price')));
            } else if (currentSort === 'price-high') {
                visibleCards.sort((a, b) => parseInt(b.getAttribute('data-price')) - parseInt(a.getAttribute('data-price')));
            } else if (currentSort === 'name') {
                visibleCards.sort((a, b) => {
                    const nameA = a.querySelector('.product-name').textContent;
                    const nameB = b.querySelector('.product-name').textContent;
                    return nameA.localeCompare(nameB);
                });
            }

            const grid = document.getElementById('productsGrid');
            visibleCards.forEach(card => grid.appendChild(card));

            document.getElementById('resultsCount').textContent = visibleCount;
        }

        function resetFilters() {
            document.getElementById('sortFilter').value = 'popular';
            document.getElementById('priceFilter').value = 'all';
            document.getElementById('sizeFilter').value = 'all';
            
            document.querySelectorAll('.genre-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector('.genre-btn').classList.add('active');
            
            currentGenre = 'all';
            applyFilters();
        }
    