document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Scroll Reveal Animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    // MODAL LOGIC
    const projectCards = document.querySelectorAll('.project-card');
    const closeButtons = document.querySelectorAll('.close-modal');
    const body = document.body;

    // Open Modal
    projectCards.forEach(card => {
        card.addEventListener('click', () => {
            const modalId = card.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                body.classList.add('modal-open');
            }
        });
    });

    // Close Modal (Button)
    closeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering other clicks
            const modal = btn.closest('.modal');
            modal.classList.remove('active');
            body.classList.remove('modal-open');
        });
    });

    // Close Modal (Click Outside)
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('active');
            body.classList.remove('modal-open');
        }
    });

    // LIGHTBOX LOGIC
    const lightbox = document.createElement('div');
    lightbox.id = 'lightbox';
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <span class="close-lightbox">&times;</span>
        <button class="lightbox-prev">&#10094;</button>
        <img id="lightbox-img" class="lightbox-img" src="" alt="Enlarged Project Image">
        <button class="lightbox-next">&#10095;</button>
        <div class="lightbox-caption"></div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.querySelector('.lightbox-caption');
    const closeLightboxBtn = document.querySelector('.close-lightbox');
    const prevBtn = document.querySelector('.lightbox-prev');
    const nextBtn = document.querySelector('.lightbox-next');

    const galleries = {};
    let currentLightboxModalId = null;
    let currentImageIndex = 0;

    projectCards.forEach(card => {
        const modalId = card.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        const cardImg = card.querySelector('.project-image img');
        
        const galleryImgs = [];
        const modalSrcs = new Set();
        
        if (modal) {
            const tempModalImages = modal.querySelectorAll('.modal-gallery img');
            tempModalImages.forEach(img => modalSrcs.add(img.src));
        }
        
        // Add card thumbnail to the lightbox gallery queue if it's not already in the modal
        if (cardImg && !modalSrcs.has(cardImg.src)) {
            galleryImgs.push({ src: cardImg.src, alt: cardImg.alt || 'Project Cover' });
        }
        
        // Add modal images to gallery
        if (modal) {
            const modalImages = modal.querySelectorAll('.modal-gallery img');
            modalImages.forEach((img) => {
                const index = galleryImgs.length;
                galleryImgs.push({ src: img.src, alt: img.alt || 'Project Image' });
                img.style.cursor = 'pointer';
                img.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    openLightbox(modalId, index);
                });
            });
        }
        
        galleries[modalId] = galleryImgs;
    });

    function openLightbox(modalId, index) {
        currentLightboxModalId = modalId;
        currentImageIndex = index;
        updateLightboxImage();
        lightbox.classList.add('active');
        body.classList.add('modal-open'); // to prevent background scrolling
    }

    function updateLightboxImage() {
        if (!currentLightboxModalId) return;
        const imgs = galleries[currentLightboxModalId];
        if (!imgs || imgs.length === 0) return;
        
        lightboxImg.src = imgs[currentImageIndex].src;
        lightboxImg.alt = imgs[currentImageIndex].alt;
        lightboxCaption.textContent = `${currentImageIndex + 1} of ${imgs.length}`;
    }

    function nextLightboxImage() {
        if (!currentLightboxModalId) return;
        const imgs = galleries[currentLightboxModalId];
        currentImageIndex = (currentImageIndex + 1) % imgs.length;
        updateLightboxImage();
    }

    function prevLightboxImage() {
        if (!currentLightboxModalId) return;
        const imgs = galleries[currentLightboxModalId];
        currentImageIndex = (currentImageIndex - 1 + imgs.length) % imgs.length;
        updateLightboxImage();
    }

    closeLightboxBtn.addEventListener('click', () => {
        closeLightbox();
    });

    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        nextLightboxImage();
    });

    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        prevLightboxImage();
    });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    function closeLightbox() {
        lightbox.classList.remove('active');
        // only remove modal-open if we are not also inside a modal
        const activeModal = document.querySelector('.modal.active');
        if (!activeModal) {
            body.classList.remove('modal-open');
        }
    }

    // Touch Support for swiping
    let touchStartX = 0;
    let touchEndX = 0;
    
    lightbox.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, {passive: true});
    
    lightbox.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, {passive: true});
    
    function handleSwipe() {
        const threshold = 50;
        if (touchStartX - touchEndX > threshold) nextLightboxImage();
        if (touchEndX - touchStartX > threshold) prevLightboxImage();
    }

    // Extend Keydown Event for Lightbox & Modal
    document.addEventListener('keydown', (e) => {
        if (lightbox.classList.contains('active')) {
            if (e.key === 'Escape') {
                closeLightbox();
            } else if (e.key === 'ArrowRight') {
                nextLightboxImage();
            } else if (e.key === 'ArrowLeft') {
                prevLightboxImage();
            }
        } else {
            // Existing modal escape logic
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal.active');
                if (activeModal) {
                    activeModal.classList.remove('active');
                    body.classList.remove('modal-open');
                }
            }
        }
    });
});
