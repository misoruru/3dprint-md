// index.js — специфичная логика главной страницы
// renderCarousel, openProductDetailModal и др. — в index.html

        // FAQ Toggle
        function toggleFaq(element) {
            const faqItem = element.parentElement;
            const isActive = faqItem.classList.contains('active');
            
            // Close all FAQ items
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                faqItem.classList.add('active');
            }
        }

        // Product price calculation
        let baseProductPrice = 0;

        function updateProductPrice() {
            const colorSelect = document.getElementById('productColor');
            const fillSelect = document.getElementById('productFill');
            const priceDisplay = document.getElementById('productPrice');
            
            if (!colorSelect || !fillSelect || !priceDisplay) return;
            
            let totalPrice = baseProductPrice;
            
            // Add color surcharge
            if (colorSelect.value === 'multicolor') {
                totalPrice += 150;
            }
            
            // Add fill surcharge
            if (fillSelect.value === 'solid') {
                totalPrice += 100;
            }
            
            priceDisplay.textContent = totalPrice;
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

        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 100) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });

        // Reveal on scroll
        const reveals = document.querySelectorAll('.reveal');
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.1 });

        reveals.forEach(reveal => revealObserver.observe(reveal));

        // Selection Modal (First popup to choose type)
        function openSelectionModal() {
            document.getElementById('selectionModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function selectOrderType(type) {
            // Close selection modal
            document.getElementById('selectionModal').classList.remove('active');
            // Open order modal with selected type
            openOrderModal(type);
        }

        // Order Type Modal
        function openOrderModal(type) {
            const modal = document.getElementById('orderTypeModal');
            const orderTypeInput = document.getElementById('orderType');
            const orderTypeDisplay = document.getElementById('orderTypeDisplay');
            const uploadLabel = document.getElementById('uploadLabel');
            const uploadText = document.getElementById('uploadText');
            const estimatedPrice = document.getElementById('estimatedPrice');
            
            orderTypeInput.value = type;
            
            if (type === 'standard') {
                orderTypeDisplay.value = 'Стандарт - Готовая 3D модель';
                uploadLabel.textContent = 'Загрузить 3D модель (STL, OBJ, 3MF)';
                uploadText.textContent = 'Загрузите вашу 3D модель';
                estimatedPrice.textContent = 'от 199 MDL';
                document.getElementById('fileInput').accept = '.stl,.obj,.3mf';
            } else if (type === 'premium') {
                orderTypeDisplay.value = 'Премиум - Создание модели по фото';
                uploadLabel.textContent = 'Загрузить фотографию (JPG, PNG)';
                uploadText.textContent = 'Загрузите фото для создания 3D модели';
                estimatedPrice.textContent = 'от 599 MDL';
                document.getElementById('fileInput').accept = '.jpg,.jpeg,.png';
            } else if (type === 'human-copy') {
                orderTypeDisplay.value = 'Эксклюзив - 3D копия человека';
                uploadLabel.textContent = 'Загрузить фотографии (JPG, PNG)';
                uploadText.textContent = 'Загрузите 3-5 фотографий человека (разные ракурсы)';
                estimatedPrice.textContent = 'от 899 MDL';
                document.getElementById('fileInput').accept = '.jpg,.jpeg,.png';
                document.getElementById('fileInput').multiple = true;
            }
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Product Modal
        function openProductModal(productName, price, emoji) {
            baseProductPrice = parseInt(price);
            document.getElementById('productName').value = productName;
            
            // Fill preview block
            document.getElementById('productPreviewName').textContent = productName;
            document.getElementById('productPreviewPrice').textContent = price;
            document.getElementById('productPreviewEmoji').textContent = emoji || '';
            
            // Reset selects to default
            document.getElementById('productColor').value = 'gray';
            document.getElementById('productFill').value = 'lattice';
            
            // Update price display
            document.getElementById('productPrice').textContent = price;
            
            document.getElementById('productModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Gallery Modal
        function openGalleryModal() {
            document.getElementById('galleryModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Close all modals
        function closeAllModals() {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.classList.remove('active');
            });
            document.body.style.overflow = 'auto';
        }

        // File upload handler
        function handleFileSelect(event) {
            const files = event.target.files;
            if (files.length > 0) {
                if (files.length === 1) {
                    document.getElementById('fileName').textContent = `Выбран файл: ${files[0].name}`;
                } else {
                    document.getElementById('fileName').textContent = `Выбрано файлов: ${files.length}`;
                }
            }
        }

        // Close modal on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal')) {
                    closeAllModals();
                }
            });
        });

        // Order Type Form submission
        document.getElementById('orderTypeForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const orderType = document.getElementById('orderType').value;
            const fileInput = document.getElementById('fileInput');
            
            if (!fileInput.files.length) {
                alert('Пожалуйста, загрузите файл');
                return;
            }
            
            let orderTypeName = '';
            if (orderType === 'standard') {
                orderTypeName = 'Стандарт - Готовая 3D модель';
            } else if (orderType === 'premium') {
                orderTypeName = 'Премиум - Создание из фото';
            } else if (orderType === 'human-copy') {
                orderTypeName = 'Эксклюзив - 3D копия человека';
            }
            
            alert(`Заказ успешно отправлен! Мы свяжемся с вами в ближайшее время.\nТип заказа: ${orderTypeName}\n\nОплата: предоплата по банковской карте`);
            closeAllModals();
            e.target.reset();
            document.getElementById('fileName').textContent = '';
        });

        // Product Form submission
        document.getElementById('productForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const productName = document.getElementById('productName').value;
            const color = document.getElementById('productColor').options[document.getElementById('productColor').selectedIndex].text;
            const fill = document.getElementById('productFill').options[document.getElementById('productFill').selectedIndex].text;
            const totalPrice = document.getElementById('productPrice').textContent;
            
            alert(`Заказ успешно оформлен!\n\nТовар: ${productName}\nЦвет: ${color}\nЗаполнение: ${fill}\nИтого: ${totalPrice} MDL\n\nОплата: предоплата по банковской карте\n\nМы свяжемся с вами в ближайшее время для подтверждения.`);
            closeAllModals();
            e.target.reset();
        });

        // Carousel drag functionality
        const carousel = document.getElementById('productCarousel');
        let isDown = false;
        let startX;
        let scrollLeft;
        let isDragging = false;

        carousel.addEventListener('mousedown', (e) => {
            // Don't start dragging if clicking on a button
            if (e.target.classList.contains('order-btn') || e.target.closest('.order-btn')) {
                return;
            }
            isDown = true;
            isDragging = false;
            carousel.style.cursor = 'grabbing';
            startX = e.pageX - carousel.offsetLeft;
            scrollLeft = carousel.scrollLeft;
        });

        carousel.addEventListener('mouseleave', () => {
            isDown = false;
            carousel.style.cursor = 'grab';
        });

        carousel.addEventListener('mouseup', () => {
            isDown = false;
            carousel.style.cursor = 'grab';
        });

        carousel.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            isDragging = true;
            const x = e.pageX - carousel.offsetLeft;
            const walk = (x - startX) * 2;
            carousel.scrollLeft = scrollLeft - walk;
        });

        // Prevent click events when dragging
        carousel.addEventListener('click', (e) => {
            if (isDragging) {
                e.preventDefault();
                e.stopPropagation();
            }
        }, true);

        // Arrow navigation
        function scrollCarousel(direction) {
            const cardWidth = carousel.querySelector('.product-card').offsetWidth;
            const gap = 32; // 2rem in pixels
            const scrollAmount = (cardWidth + gap) * direction;
            carousel.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            // Check if carousel is in viewport
            const rect = carousel.getBoundingClientRect();
            const isInViewport = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isInViewport) {
                if (e.key === 'ArrowLeft') {
                    scrollCarousel(-1);
                } else if (e.key === 'ArrowRight') {
                    scrollCarousel(1);
                }
            }
        });

        // ============================================
        // INTERACTIVE STARRY NIGHT BACKGROUND
        // ============================================
        const canvas = document.getElementById('starryCanvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Star class
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
                // Twinkling effect
                this.twinklePhase += this.twinkleSpeed;
                this.opacity = 0.3 + Math.sin(this.twinklePhase) * 0.3;

                // Mouse interaction - stars move away from cursor
                const dx = this.x - mouseX;
                const dy = this.y - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const maxDistance = 150;

                if (distance < maxDistance) {
                    const force = (maxDistance - distance) / maxDistance;
                    this.x += (dx / distance) * force * 2;
                    this.y += (dy / distance) * force * 2;
                }

                // Slow drift
                this.y += this.speed;

                // Reset if out of bounds
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
                
                // Glow effect
                const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 3);
                gradient.addColorStop(0, `rgba(0, 240, 255, ${this.opacity})`);
                gradient.addColorStop(0.5, `rgba(157, 78, 221, ${this.opacity * 0.3})`);
                gradient.addColorStop(1, 'rgba(0, 240, 255, 0)');
                
                ctx.fillStyle = gradient;
                ctx.fill();
            }
        }

        // Shooting star class
        class ShootingStar {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.length = Math.random() * 80 + 40;
                this.speed = Math.random() * 15 + 10;
                this.angle = Math.random() * Math.PI / 4 + Math.PI / 6; // 30-75 degrees
                this.opacity = 1;
                this.fadeSpeed = 0.02;
            }

            update() {
                this.x += Math.cos(this.angle) * this.speed;
                this.y += Math.sin(this.angle) * this.speed;
                this.opacity -= this.fadeSpeed;
            }

            draw() {
                ctx.beginPath();
                ctx.moveTo(this.x, this.y);
                ctx.lineTo(
                    this.x - Math.cos(this.angle) * this.length,
                    this.y - Math.sin(this.angle) * this.length
                );
                
                const gradient = ctx.createLinearGradient(
                    this.x, this.y,
                    this.x - Math.cos(this.angle) * this.length,
                    this.y - Math.sin(this.angle) * this.length
                );
                gradient.addColorStop(0, `rgba(255, 255, 255, ${this.opacity})`);
                gradient.addColorStop(0.5, `rgba(0, 240, 255, ${this.opacity * 0.6})`);
                gradient.addColorStop(1, `rgba(0, 240, 255, 0)`);
                
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            isDead() {
                return this.opacity <= 0;
            }
        }

        // Ripple effect on click
        class Ripple {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.radius = 0;
                this.maxRadius = 100;
                this.speed = 3;
                this.opacity = 0.8;
            }

            update() {
                this.radius += this.speed;
                this.opacity -= 0.02;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(0, 240, 255, ${this.opacity})`;
                ctx.lineWidth = 2;
                ctx.stroke();

                // Inner ripple
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius * 0.7, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(157, 78, 221, ${this.opacity * 0.5})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }

            isDead() {
                return this.opacity <= 0 || this.radius >= this.maxRadius;
            }
        }

        // Initialize stars
        const stars = [];
        const starCount = 150;
        for (let i = 0; i < starCount; i++) {
            stars.push(new Star());
        }

        const shootingStars = [];
        const ripples = [];
        let mouseX = canvas.width / 2;
        let mouseY = canvas.height / 2;

        // Mouse move tracking on entire document
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // Click creates ripple effect and nearby stars burst
        // Works everywhere except on interactive elements
        document.addEventListener('click', (e) => {
            // Get element that was clicked
            const clickedElement = e.target;
            
            // Check if clicked element is interactive (button, link, input, etc)
            const isInteractive = clickedElement.closest('button, a, input, textarea, select, .product-card, .service-card, .modal, nav');
            
            // Only create effects if NOT clicking interactive elements
            if (!isInteractive) {
                ripples.push(new Ripple(e.clientX, e.clientY));
                
                // Create particle burst
                stars.forEach(star => {
                    const dx = star.x - e.clientX;
                    const dy = star.y - e.clientY;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 100) {
                        const force = (100 - distance) / 100;
                        star.x += (dx / distance) * force * 50;
                        star.y += (dy / distance) * force * 50;
                    }
                });
            }
        });

        // Random shooting stars
        setInterval(() => {
            if (Math.random() < 0.3) {
                shootingStars.push(new ShootingStar(
                    Math.random() * canvas.width * 0.5,
                    Math.random() * canvas.height * 0.3
                ));
            }
        }, 3000);

        // Animation loop
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Update and draw stars
            stars.forEach(star => {
                star.update(mouseX, mouseY);
                star.draw();
            });

            // Update and draw shooting stars
            for (let i = shootingStars.length - 1; i >= 0; i--) {
                shootingStars[i].update();
                shootingStars[i].draw();
                if (shootingStars[i].isDead()) {
                    shootingStars.splice(i, 1);
                }
            }

            // Update and draw ripples
            for (let i = ripples.length - 1; i >= 0; i--) {
                ripples[i].update();
                ripples[i].draw();
                if (ripples[i].isDead()) {
                    ripples.splice(i, 1);
                }
            }

            requestAnimationFrame(animate);
        }

        animate();
