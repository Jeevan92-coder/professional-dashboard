// Login Page JavaScript

// Toggle password visibility
function togglePassword() {
    const field = document.getElementById('password');
    if (field.type === 'password') {
        field.type = 'text';
    } else {
        field.type = 'password';
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const loginIdentifier = document.getElementById('login_identifier').value.trim();
            const password = document.getElementById('password').value;
            
            // Check if fields are filled
            if (!loginIdentifier) {
                e.preventDefault();
                alert('❌ Please enter username/email/mobile!');
                return false;
            }
            
            if (!password) {
                e.preventDefault();
                alert('❌ Please enter password!');
                return false;
            }
            
            // Show loading
            const btn = form.querySelector('.submit-btn');
            btn.disabled = true;
            btn.textContent = 'Logging in... ⏳';
        });
    }
});

// Auto focus first input
document.addEventListener('DOMContentLoaded', function() {
    const firstInput = document.querySelector('input');
    if (firstInput) {
        firstInput.focus();
    }
});