// Main JavaScript file

// Contact form handling
document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const formData = new FormData(contactForm);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };

            // In a real application, you would send this data to a server
            console.log('Form submitted:', data);

            // Show success message
            alert(`Спасибо за обращение, ${data.name}!\n\nМы получили ваше сообщение и свяжемся с вами в ближайшее время по адресу ${data.email}.`);

            // Reset form
            contactForm.reset();
        });
    }
});

// Mobile menu toggle (for future enhancement)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation for product images
function addImageLoadAnimation() {
    const productImages = document.querySelectorAll('.product-image');
    productImages.forEach((img, index) => {
        img.style.animationDelay = `${index * 0.1}s`;
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    addImageLoadAnimation();
});

// Utility function for formatting numbers
function formatNumber(num) {
    return num.toLocaleString('ru-RU');
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Lazy loading animation on scroll
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.feature-card, .product-card');
    elements.forEach(element => {
        if (isInViewport(element)) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
});
