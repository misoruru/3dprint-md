// starry-bg.js — анимированный звёздный фон (общий для всех страниц)

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
    