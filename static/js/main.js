// ========== HIDE LOADER IMMEDIATELY ==========
// This ensures loader disappears as soon as possible
window.addEventListener('load', function() {
    const loader = document.querySelector('.loader');
    if(loader) {
        loader.style.opacity = '0';
        loader.style.visibility = 'hidden';
        loader.style.display = 'none';
    }
});

// Also hide loader immediately if DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const loader = document.querySelector('.loader');
    if(loader) {
        setTimeout(function() {
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
            loader.style.display = 'none';
        }, 500);
    }
});

// ========== INITIALIZE AOS ==========
AOS.init({
    duration: 1000,
    once: true,
    offset: 100
});

// ========== CREATE PARTICLES ==========
function createParticles() {
    const container = document.querySelector('.particles');
    if(!container) return;
    for(let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = 5 + Math.random() * 5 + 's';
        container.appendChild(particle);
    }
}
createParticles();

// ========== CUSTOM CURSOR ==========
const cursor = document.querySelector('.cursor');
const cursorDot = document.querySelector('.cursor-dot');

if(cursor && cursorDot) {
    document.addEventListener('mousemove', (e) => {
        cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
        cursorDot.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    });
    
    document.querySelectorAll('a, button, .team-card, .service-card, .pricing-card, .feature-card').forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.width = '50px';
            cursor.style.height = '50px';
            cursor.style.border = '2px solid var(--primary)';
            cursor.style.background = 'rgba(99, 102, 241, 0.1)';
        });
        el.addEventListener('mouseleave', () => {
            cursor.style.width = '30px';
            cursor.style.height = '30px';
            cursor.style.background = 'transparent';
        });
    });
}

// ========== NAVBAR SCROLL EFFECT ==========
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if(navbar && window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else if(navbar) {
        navbar.classList.remove('scrolled');
    }
});

// ========== COUNTER ANIMATION ==========
const counters = document.querySelectorAll('.stat-number');

const animateNumber = (el) => {
    const target = parseInt(el.innerText);
    if(isNaN(target)) return;
    let current = 0;
    const increment = target / 50;
    const updateCounter = () => {
        if(current < target) {
            current += increment;
            el.innerText = Math.ceil(current);
            setTimeout(updateCounter, 30);
        } else {
            el.innerText = target;
        }
    };
    updateCounter();
};

const observerOptions = { threshold: 0.5 };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            animateNumber(entry.target);
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

counters.forEach(counter => {
    observer.observe(counter);
});

// ========== HAMBURGER MENU ==========
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if(hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks?.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks?.classList.remove('active');
        hamburger?.classList.remove('active');
    });
});

// ========== SMOOTH SCROLL ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if(target) {
            target.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
            navLinks?.classList.remove('active');
            hamburger?.classList.remove('active');
        }
    });
});

// ========== 3D TILT EFFECT ==========
const cards = document.querySelectorAll('.team-card, .service-card, .pricing-card, .feature-card');
cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
    });
});

// ========== TYPED ANIMATION ==========
const typedText = document.querySelector('.hero-title .gradient-text');
if (typedText) {
    typedText.style.opacity = '0';
    setTimeout(() => {
        typedText.style.opacity = '1';
        typedText.style.transition = 'opacity 0.5s ease';
    }, 500);
}

// ========== ADD DATA-TARGET TO STATS ==========
document.querySelectorAll('.stat-number').forEach(stat => {
    const text = stat.textContent;
    const number = parseInt(text);
    if (!isNaN(number) && number > 0 && number < 1000) {
        stat.setAttribute('data-target', number);
        stat.textContent = '0';
    }
});

console.log('Nexvion website loaded successfully! 🚀');
