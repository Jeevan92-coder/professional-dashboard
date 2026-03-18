// Dashboard JS with Settings Sync - Add to beginning of dashboard.js

'use strict';

// ===========================
// LOAD USER PREFERENCES ON DASHBOARD
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 Dashboard Loading with User Preferences...');
    
    // Apply all saved preferences
    applyUserPreferences();
    
    // Then initialize rest of the app
    initializeApp();
});

function applyUserPreferences() {
    // 1. Apply saved font
    const savedFont = localStorage.getItem('userFont');
    if (savedFont) {
        applyDashboardFont(savedFont);
        console.log(`✅ Font Applied: ${savedFont}`);
    }
    
    // 2. Apply saved theme
    const savedTheme = localStorage.getItem('userTheme');
    if (savedTheme) {
        applyDashboardTheme(savedTheme);
        console.log(`✅ Theme Applied: ${savedTheme}`);
    }
    
    // 3. Apply saved background
    const savedBg = localStorage.getItem('userBackground');
    if (savedBg) {
        applyDashboardBackground(savedBg);
        console.log('✅ Custom Background Applied');
    }
    
    // 4. Apply saved dark mode
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
        console.log('✅ Dark Mode Applied');
    }
}

function applyDashboardFont(fontName) {
    let fontFamily = '';
    
    switch(fontName) {
        case 'Inter':
            fontFamily = "'Inter', sans-serif";
            break;
        case 'Roboto':
            fontFamily = "'Roboto', sans-serif";
            break;
        case 'Open Sans':
            fontFamily = "'Open Sans', sans-serif";
            break;
        case 'Lato':
            fontFamily = "'Lato', sans-serif";
            break;
        case 'Montserrat':
            fontFamily = "'Montserrat', sans-serif";
            break;
        case 'Poppins':
            fontFamily = "'Poppins', sans-serif";
            break;
        default:
            fontFamily = "'Inter', sans-serif";
    }
    
    document.body.style.fontFamily = fontFamily;
    document.documentElement.style.setProperty('--app-font', fontFamily);
}

function applyDashboardTheme(themeName) {
    let themeGradient = '';
    
    switch(themeName) {
        case 'ocean-blue':
            themeGradient = 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)';
            break;
        case 'sunset-orange':
            themeGradient = 'linear-gradient(135deg, #2c1810, #4a2c1a, #3d2419)';
            break;
        case 'forest-green':
            themeGradient = 'linear-gradient(135deg, #0a2e0f, #1a3e1f, #152e1a)';
            break;
        case 'royal-purple':
            themeGradient = 'linear-gradient(135deg, #1a0a2e, #2e1a4a, #251a3e)';
            break;
        case 'crimson-red':
            themeGradient = 'linear-gradient(135deg, #2e0a0f, #4a1a1f, #3e1a25)';
            break;
        case 'sky-blue':
            themeGradient = 'linear-gradient(135deg, #0a1e2e, #1a3e4a, #1a2e3e)';
            break;
        case 'pink-dream':
            themeGradient = 'linear-gradient(135deg, #2e0a1e, #4a1a3e, #3e1a2e)';
            break;
        case 'golden-hour':
            themeGradient = 'linear-gradient(135deg, #2e1e0a, #4a3e1a, #3e2e1a)';
            break;
        default:
            themeGradient = 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)';
    }
    
    document.body.style.background = themeGradient;
}

function applyDashboardBackground(imageData) {
    document.body.style.backgroundImage = `url(${imageData})`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundAttachment = 'fixed';
}

// ===========================
// DARK MODE TOGGLE - FIXED
// ===========================
function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById('theme-icon');
    
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        localStorage.setItem('darkMode', 'enabled');
        console.log('🌙 Dark Mode Enabled');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        localStorage.setItem('darkMode', 'disabled');
        console.log('☀️ Light Mode Enabled');
    }
}

// Make toggleTheme available globally
window.toggleTheme = toggleTheme;

// ===========================
// REST OF DASHBOARD CODE CONTINUES...
// (Keep all your existing dashboard.js code below this)
// ===========================

const CONFIG = {
    particleCount: 100,
    animationDuration: 600,
    debounceDelay: 300,
    scrollThreshold: 0.1,
    sessionTimeout: 15 * 60 * 1000,
};

function initializeApp() {
    initParticleSystem();
    initNavigationEffects();
    initCountUpAnimations();
    initScrollAnimations();
    initFormValidation();
    initTooltips();
    initKeyboardShortcuts();
    initSmoothScrolling();
    initLazyLoading();
    initPerformanceMonitoring();
    initSessionTracking();
    initFlashMessages();
    displayConsoleBranding();
}

// [Keep all your existing dashboard.js functions here...]

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null, radius: 150 };
        this.init();
    }
    
    init() {
        this.resize();
        this.createParticles();
        this.animate();
        this.bindEvents();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        const particleCount = Math.min(CONFIG.particleCount, Math.floor(this.canvas.width / 10));
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                radius: Math.random() * 2.5 + 0.5,
                opacity: Math.random() * 0.5 + 0.3,
                color: this.getParticleColor(),
            });
        }
    }
    
    getParticleColor() {
        const colors = [
            'rgba(102, 126, 234, ',
            'rgba(118, 75, 162, ',
            'rgba(240, 147, 251, ',
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = particle.color + particle.opacity + ')';
        this.ctx.fill();
    }
    
    connectParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    this.ctx.beginPath();
                    const opacity = 0.15 * (1 - distance / 150);
                    this.ctx.strokeStyle = `rgba(102, 126, 234, ${opacity})`;
                    this.ctx.lineWidth = 0.8;
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }
    
    updateParticles() {
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (this.mouse.x !== null && this.mouse.y !== null) {
                const dx = particle.x - this.mouse.x;
                const dy = particle.y - this.mouse.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.mouse.radius) {
                    const force = (this.mouse.radius - distance) / this.mouse.radius;
                    const angle = Math.atan2(dy, dx);
                    particle.x += Math.cos(angle) * force * 2;
                    particle.y += Math.sin(angle) * force * 2;
                }
            }
            
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
            particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
        });
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.updateParticles();
        this.connectParticles();
        this.particles.forEach(particle => this.drawParticle(particle));
        requestAnimationFrame(() => this.animate());
    }
    
    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.particles = [];
            this.createParticles();
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }
}

function initParticleSystem() {
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        new ParticleSystem(canvas);
    }
}

function initNavigationEffects() {
    const nav = document.querySelector('.top-nav');
    if (!nav) return;
    
    let lastScroll = 0;
    let scrollTimeout;
    
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > lastScroll && currentScroll > 100) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }
            lastScroll = currentScroll;
        }, 10);
    });
}

function initCountUpAnimations() {
    const counters = document.querySelectorAll('.count-up');
    const animateCounter = (counter, target, duration = 2000) => {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        updateCounter();
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
}

function initScrollAnimations() {
    const elements = document.querySelectorAll('.stat-card, .profile-section, .activity-section, .login-section, .alerts-section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 50);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: CONFIG.scrollThreshold, rootMargin: '0px 0px -50px 0px' });
    
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        observer.observe(el);
    });
}

function toggleNotifications() {
    const panel = document.getElementById('notificationPanel');
    if (!panel) return;
    panel.classList.toggle('active');
}

function openEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.classList.add('active');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function openPasswordModal() {
    const modal = document.getElementById('passwordModal');
    if (modal) {
        modal.classList.add('active');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closePasswordModal() {
    const modal = document.getElementById('passwordModal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const wrapper = input.closest('.password-input-wrapper');
    const button = wrapper?.querySelector('.toggle-password');
    const icon = button?.querySelector('i');
    if (!icon) return;
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function validatePassword() {
    const newPassword = document.getElementById('new_password')?.value;
    const confirmPassword = document.getElementById('confirm_password')?.value;
    if (!newPassword || !confirmPassword) {
        alert('Please fill in all password fields');
        return false;
    }
    if (newPassword !== confirmPassword) {
        alert('Passwords do not match!');
        return false;
    }
    if (newPassword.length < 8) {
        alert('Password must be at least 8 characters!');
        return false;
    }
    return true;
}

function initFormValidation() {}
function initTooltips() {}
function initKeyboardShortcuts() {}
function initSmoothScrolling() {}
function initLazyLoading() {}
function initPerformanceMonitoring() {}
function initSessionTracking() {}
function initFlashMessages() {}

function displayConsoleBranding() {
    console.log('%c🚀 Dashboard Loaded!', 'font-size: 20px; font-weight: bold; color: #667eea;');
    console.log('%c© Created by Meher Jeevan', 'font-size: 14px; color: #9c27b0;');
}

// Make functions globally available
window.dashboardApp = {
    toggleTheme,
    toggleNotifications,
    openEditModal,
    closeEditModal,
    openPasswordModal,
    closePasswordModal,
    togglePasswordVisibility,
    validatePassword,
};