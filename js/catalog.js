// catalog.js — специфичная логика каталога
// renderProductsGrid, openProductDetailModal и др. — в catalog.html

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
            renderImageInto(document.getElementById('productDetailMainImage'), currentProductData.images[index]);
            
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

// Card click handlers are set inline via onclick in renderProductsGrid()

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
